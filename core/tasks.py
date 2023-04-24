import datetime as dt
import functools

import pytz
import requests
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Value, JSONField, Q
from django.utils.translation import gettext_lazy as _l
from django.utils.translation import ngettext
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

from core.models import Announcement, User, Event
from metropolis.celery import app

logger = get_task_logger(__name__)
session = requests.Session()
session.headers.update(
    {
        # "Authorization": f"Bearer {os.getenv('EXPO_TOKEN')}",# TODO: expo push notifications authn?
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)
for m in ("get", "options", "head", "post", "put", "patch", "delete"):
    setattr(
        session,
        m,
        functools.partial(
            getattr(session, m), timeout=settings.NOTIF_EXPO_TIMEOUT_SECS
        ),
    )


def users_with_token():
    return User.objects.filter(not Q(expo_notif_tokens=Value({}, JSONField())))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=4, minute=0), notif_events_singleday)


@app.task
def notif_broker_announcement(obj_id):
    logger.info(f"notif_broker_announcement for {obj_id}")
    ann = Announcement.objects.get(id=obj_id)
    affected = users_with_token()
    category = ""
    if ann.organization.id in settings.ANNOUNCEMENTS_NOTIFY_FEEDS:
        category = "ann.public"
    else:
        affected = affected.filter(
            Q(tags_following__in=ann.tags.all())
            | Q(organizations__in=[ann.organization])
        )
        category = "ann.personal"
    logger.info(f"notif_broker_announcement2 for {obj_id} affects {u}")
    for u in affected.all():
        notif_single.delay(
            u.id,
            dict(
                title=_l("New Announcement: %(title)s") % dict(title=ann.title),
                body=ann.body,
                category=category,
            ),
        )
    notif_events_singleday.delay()


@app.task
def notif_events_singleday(date: dt.date = None):
    tz = pytz.timezone(settings.TIME_ZONE)
    if date is None:
        date = dt.date.today()
    eligible = users_with_token()
    for u in eligible.all():
        # assume we don't have 10 million events overlapping a single day (we can't fit it in a single notif aniway)
        date_mintime = dt.datetime.combine(date, dt.datetime.min.time()).astimezone(tz)
        date_maxtime = dt.datetime.combine(date, dt.datetime.max.time()).astimezone(tz)
        covering = list(
            Event.get_events(u)
            .filter(
                start_date__lte=date_maxtime,
                end_date__gte=date_mintime,
            )
            .all()
        )
        if len(covering) == 0:
            continue
        covering.sort(key=lambda e: int(e.schedule_format == "default"))
        covering.sort(key=lambda e: e.start_date - date_mintime)
        body = ngettext(
            "%(count)d Event:\n",
            "%(count)d Events:\n",
            len(covering),
        ) % dict(count=len(covering))
        for i, e in enumerate(covering):
            body += _l("%(i)d. %(title)s\n") % dict(i=i + 1, title=e.name)
        headline = covering[0]
        notif_single.delay(
            u.id,
            dict(
                title=_l("%(date)s: %(headline)s")
                % dict(date=date.strftime("%a %b %d"), headline=headline.name),
                body=body,
                category="event.singleday",
            ),
        )


@app.task(bind=True)
def notif_single(self, recipient_id: int, msg_kwargs):
    recipient = User.objects.get(id=recipient_id)
    if settings.NOTIF_DRY_RUN:
        logger.info(
            f"notif_single to {recipient} ({recipient.expo_notif_tokens}): {msg_kwargs}"
        )
        return
    notreg_tokens = set()
    for token in recipient.expo_notif_tokens:
        try:
            resp = PushClient(session=session).publish(
                PushMessage(to=f"ExponentPushToken[{token}]", **msg_kwargs)
            )
        except (ConnectionError, HTTPError) as exc:
            raise self.retry(exc=exc)
        try:
            resp.validate_response()
        except DeviceNotRegisteredError:
            notreg_tokens.add(token)
        except PushTicketError as exc:
            raise self.retry(exc=exc)
    if notreg_tokens:
        u = User.objects.filter(id=recipient_id)
        for token in notreg_tokens:
            del u.expo_notif_tokens[token]
        u.save()
