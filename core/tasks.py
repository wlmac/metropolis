import datetime as dt
import functools
from pathlib import Path

import pytz
import requests
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import F, JSONField, Q, Value
from django.db.models.functions.text import Concat
from django.utils import timezone
from django.utils.translation import gettext_lazy as _l
from django.utils.translation import ngettext
from django.core.exceptions import ObjectDoesNotExist
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from json import dumps, loads

from core.models import (
    Announcement,
    BlogPost,
    Comment,
    Event,
    Term,
    User,
    Organization,
    Tag,
)
from core.utils.tasks import get_random_username
from core.utils.ai import prompt_gemini
from metropolis.celery import app

logger = get_task_logger(__name__)
session = requests.Session()
session.headers.update(
    {
        # "Authorization": f"Bearer {os.getenv('EXPO_TOKEN')}", # TODO: expo push notifications authn?
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
    return User.objects.exclude(Q(expo_notif_tokens=Value({}, JSONField())))


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0), delete_expired_users)
    sender.add_periodic_task(crontab(hour=18, minute=0), notif_events_singleday)
    sender.add_periodic_task(crontab(day_of_month=1), run_group_migrations)
    sender.add_periodic_task(
        crontab(hour=1, minute=0), oauth2_clear_expired
    )  # Delete expired oauth2 tokens from db everyday at 1am

    # sender.add_periodic_task(
    #     crontab(hour=8, minute=0, day_of_week="mon-fri"), fetch_announcements
    # )

    sender.add_periodic_task(crontab(hour=4, minute=0), fetch_calendar_events)


@app.task
def delete_expired_users():
    """Scrub user data from inactive accounts that have not logged in for 14 days. (marked deleted)"""
    queryset = User.objects.filter(
        is_deleted=True,
        last_login__lt=dt.datetime.now() - dt.timedelta(days=14),
    )
    comments = Comment.objects.filter(author__in=queryset)
    comments.update(
        body=None, last_modified=timezone.now()
    )  # if body is None "deleted on %last_modified% would be shown
    queryset.update(  # We need to object to not break posts or comments
        first_name="Deleted",
        last_name="User",
        username=get_random_username(),
        bio="",
        timezone="",
        graduating_year=None,
        is_teacher=False,
        organizations=[],
        tags_following=[],
        qltrs=None,
        saved_blogs=[],
        saved_announcements=[],
        expo_notif_tokens={},
    )
    queryset.update(email=Concat(F("random_username"), Value("@maclyonsden.com")))


@app.task
def run_group_migrations():
    from scripts.migrations import migrate_groups

    print(migrate_groups())


@app.task
def notif_broker_announcement(obj_id):
    if not settings.NOTIFICATIONS_ENABLED:
        return
    logger.info(f"notif_broker_announcement for {obj_id}")
    try:
        ann = Announcement.objects.get(id=obj_id)
    except Announcement.DoesNotExist:
        logger.warning(
            f"notif_broker_announcement: announcement {obj_id} does not exist"
        )
        return
    affected = users_with_token()
    if ann.organization.id in settings.ANNOUNCEMENTS_NOTIFY_FEEDS:
        category = "ann.public"
    else:
        affected = affected.filter(
            Q(tags_following__in=ann.tags.all())
            | Q(organizations__in=[ann.organization])
        )
        category = "ann.personal"
    for u in affected.all():
        notif_single.delay(
            u.id,
            dict(
                title=_l("New Announcement: %(title)s") % dict(title=ann.title),
                body=ann.body,
                category=category,
            ),
        )


@app.task
def notif_broker_blogpost(obj_id):
    logger.info(f"notif_broker_blogpost for {obj_id}")
    try:
        post = BlogPost.objects.get(id=obj_id)
    except BlogPost.DoesNotExist:
        logger.warning(f"notif_broker_blogpost: blogpost {obj_id} does not exist")
        return
    if settings.NOTIFICATIONS_ENABLED:
        affected = users_with_token()
        for u in affected.all():
            notif_single.delay(
                u.id,
                dict(
                    title=_l("New Blog Post: %(title)s") % dict(title=post.title),
                    body=post.body,
                    category="blog",
                ),
            )


@app.task
def notif_events_singleday(date: dt.date = None):
    if not settings.NOTIFICATIONS_ENABLED:
        return
    tz = pytz.timezone(settings.TIME_ZONE)
    if date is None:
        date = dt.date.today() + dt.timedelta(days=1)
    elif isinstance(date, str):  # ken things
        date = dt.datetime.fromisoformat(date)
        raise RuntimeError(f"date {type(date)} {date}")
    eligible = users_with_token()
    for u in eligible.all():
        # assume we don't have 10 million events overlapping a single day (we can't fit it in a single notif aniway)
        date_mintime = tz.localize(dt.datetime.combine(date, dt.datetime.min.time()))
        date_maxtime = tz.localize(dt.datetime.combine(date, dt.datetime.max.time()))
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
    if not settings.NOTIFICATIONS_ENABLED:
        return
    recipient = User.objects.get(id=recipient_id)
    logger.info(
        f"notif_single to {recipient} ({recipient.expo_notif_tokens}): {msg_kwargs}"
        + ("(dry run)" if settings.NOTIF_DRY_RUN else "")
    )
    if settings.NOTIF_DRY_RUN:
        return
    notreg_tokens = set()
    for token, options in recipient.expo_notif_tokens.items():
        if options is not None:
            allowlist = options.get("allow")
            if (
                isinstance(allowlist, dict)
                and msg_kwargs["category"] not in allowlist.keys()
            ):
                logger.info(
                    f"notif_single (category {msg_kwargs['category']}) not allowed to {recipient} (allowlist {allowlist}) ({recipient.expo_notif_tokens}): {msg_kwargs}"
                    + ("(dry run)" if settings.NOTIF_DRY_RUN else "")
                )
                continue
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
        u = User.objects.filter(id=recipient_id).first()
        for token in notreg_tokens:
            del u.expo_notif_tokens[token]
        u.save()


def load_creds() -> tuple[Credentials | None, str | None, bool]:
    """
    Returns credentials from authorized_user.json file

    :returns: Tuple with the creds, error message and
    whether the client secret file exists
    """

    CLIENT_PATH = settings.SECRETS_PATH + "/client_secret.json"
    AUTHORIZED_PATH = settings.SECRETS_PATH + "/authorized_user.json"

    if not Path(settings.SECRETS_PATH).is_dir():
        return (None, f"{settings.SECRETS_PATH} directory does not exist", False)

    if not Path(CLIENT_PATH).is_file():
        return (None, f"{CLIENT_PATH} does not exist", False)

    scopes = settings.GOOGLE_SCOPES

    if Path(AUTHORIZED_PATH).is_file():
        creds = None

        try:
            creds = Credentials.from_authorized_user_file(AUTHORIZED_PATH, scopes)
        except Exception:
            return (None, "Failed to load credentials", True)

        if not creds.valid and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return (None, "Failed to refresh credentials", True)

            with open(AUTHORIZED_PATH, "w") as f:
                f.write(creds.to_json())

        return (creds, None, True)

    else:
        return (None, "No file to load client from", True)


@app.task
def oauth2_clear_expired():
    from oauth2_provider.models import clear_expired

    clear_expired()


@app.task
def fetch_announcements():
    if settings.GOOGLE_SHEET_ID == "" or settings.GOOGLE_SHEET_ID is None:
        logger.warning("Fetch Announcements: GOOGLE_SHEET_ID is empty")
        return

    creds, error_msg, client_path_exists = load_creds()

    if creds is None:
        if client_path_exists:
            logger.warning(f"Fetch Announcements: {error_msg} - Run auth_google to fix")
        else:
            logger.warning(f"Fetch Announcements: {error_msg}")
        return

    client = gspread.authorize(creds)
    worksheet = None

    try:
        worksheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
    except Exception:
        logger.warning("Fetch Announcements: Failed to open google sheet")
        return

    row_counter = 1

    row_data = []

    while True:
        data = []

        try:
            data = [value.strip() for value in worksheet.row_values(row_counter)]
        except Exception:
            logger.warning(f"Fetch Announcements: Failed to read row {row_counter}")
            break

        if row_counter == 1:
            if data != [
                "Timestamp",
                "Email Address",
                "Today's Date",
                "Student Name (First and Last Name), if applicable.",
                "Staff Advisor",
                "Club",
                "Start Date announcement is to be read (max. 3 consecutive school days).",
                "End Date announcement is to be read (NOTE: if announcement is to be read ONE DAY only, please enter the same date)",
                "Announcement to be read (max 75 words)",
            ]:
                logger.warning("Fetch Announcements: Header row does not match")
                break
        else:
            if data == []:
                break
            else:
                try:
                    parsed_data = {"body": data[8], "club_name": data[5], "status": "a"}

                    author = User.objects.filter(email=data[1]).first()

                    parsed_data["author"] = author

                    show_after = timezone.make_aware(
                        dt.datetime.strptime(data[6], "%m/%d/%Y")
                    )
                    parsed_data["show_after"] = show_after

                    row_data.append(parsed_data)
                except Exception:
                    logger.warning(
                        f"Fetch Announcements: Failed to parse row {row_counter}"
                    )

        row_counter += 1

    prompt_data = []
    organizations = (
        [organization.name for organization in Organization.objects.all()],
    )

    for parsed in row_data:
        prompt_data.append({"body": parsed["body"], "club_name": parsed["club_name"]})

    prompt = f"You are a meticulous and organized secretary at a Canadian high school. Your job is to accurately assign titles to announcements and figure out which club that announcement belongs to. Accuracy and consistency are paramount. The titles should be no more than 64 characters long. It should be descriptive of the announcement itself. Do not go over the limit. You will be provided an array of announcements. Each element in the array will contain the data for one announcement. The element will be in the format of a json object containing the body (what will be announced out) and the club_name (students may mistype clubs names, etc so you will need to pick which one you think they were trying to reference). The available names of all the clubs of the school will be provided below to you in the format of an array (E.g. ['club name 1', 'club name 2', 'club name 3', ... ]). \nWhen outputting, output a single array object. The array order must match the order of the one provided to you. DO NOT CHANGE THE ORDER UNDER ANY CIRCUMSTANCE. The array format should be the same as announcements array given to you. Each element are to be a json object, one key will be the title and the other will be the club name. Should no club match the one the student was trying to pick, then and ONLY then will you put down the club name they have listed. In this scenario, please output it in pascal case and remove any unnecessary information that is not relating to the club name itself. For example, if it's written as 'CLUB NAME (OTHER INFORMATION)', it should be outputted as just 'Club Name'. If you do find a club name in the club name array that matches the one the student was trying to write, it should be EXACTLY the same during output. Do not output anything besides the array.\nClub names: {organizations}\nAnnouncements to be titled: {dumps(prompt_data)}"

    try:
        response = prompt_gemini(prompt, model="models/gemini-2.5-flash")
        response = response.text.replace("```json", "").replace("```", "")
        response = loads(response)
    except Exception:
        logger.warning("Fetch Announcement: Something went wrong with the AI")

    try:
        for index, el in enumerate(response):
            data = row_data[index]

            try:
                org = Organization.objects.get(name=el["club_name"])
                data["organization"] = org

                if data["author"] is None:
                    data["author"] = org.owners.all()[0]
            except ObjectDoesNotExist:
                data["organization_string"] = el["club_name"]

            data["title"] = el["title"]
            del data["club_name"]

            Announcement.objects.get_or_create(body=data["body"], defaults=data)
    except Exception:
        logger.warning("Fetch Announcement: Something went wrong creating the object")


@app.task
def fetch_calendar_events():
    import traceback

    try:
        url = f"https://www.googleapis.com/calendar/v3/calendars/{settings.GCAL_CID}/events"
        url += "?fields=items(id,status,summary,description,start,end)"
        time_min = dt.datetime.now(dt.UTC) + dt.timedelta(days=-60)
        time_max = dt.datetime.now(dt.UTC) + dt.timedelta(days=60)
        params = {
            "key": settings.GCAL_API_KEY,
            "orderBy": "startTime",
            "timeMin": time_min.isoformat(),
            "timeMax": time_max.isoformat(),
            "eventTypes": "default",
            "singleEvents": "True",
            "showDeleted": "True",
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(
                f"{str(response.status_code)} - Failed to fetch calendar events"
            )

        gcal_eventlist = response.json().get("items", [])

    except Exception as exc:
        logger.warning(f"Fetch Calendar Events: {exc}")
        return

    school_org = Organization.objects.get(pk=2)  # SAC: https://maclyonsden.com/c/2

    existing_events = {
        event.gcal_id: event
        for event in Event.objects.filter(
            gcal_id__isnull=False,
            # Google calendar API returns events that overlap the time range, not just those that are within the range
            end_date__gte=time_min.isoformat(),
            start_date__lte=time_max.isoformat(),
        )
    }
    terms = list(
        Term.objects.filter(
            end_date__gte=time_min.date().isoformat(),
            start_date__lte=time_max.date().isoformat(),
        )
    )

    events_to_create = []
    events_to_update = []
    events_to_delete = []

    for gcal_event in gcal_eventlist:
        if gcal_event.get("summary").strip().lower() in ["day 1", "day 2"]:
            continue

        try:
            gcal_id = gcal_event.get("id")
            status = gcal_event.get("status")
            existing_event = existing_events.get(gcal_id)

            if existing_event is not None and (status is None or status == "cancelled"):
                events_to_delete.append(existing_event)

            if status != "confirmed":
                continue

            gcal_start = gcal_event.get("start")
            gcal_end = gcal_event.get("end")
            all_day_event = gcal_start.get("dateTime") is None

            if all_day_event:
                start_dtime = timezone.make_aware(
                    dt.datetime.combine(
                        dt.date.fromisoformat(gcal_start.get("date")),
                        dt.time(0, 0),
                    )
                )
                end_dtime = timezone.make_aware(
                    dt.datetime.combine(
                        dt.date.fromisoformat(gcal_end.get("date"))
                        + dt.timedelta(days=-1),
                        dt.time(23, 59),
                    )
                )
            else:
                start_dtime = dt.datetime.fromisoformat(gcal_start.get("dateTime"))
                end_dtime = dt.datetime.fromisoformat(gcal_end.get("dateTime"))

            event_term = next(
                (
                    term
                    for term in terms
                    if (
                        term.start_date
                        <= start_dtime.date()
                        <= end_dtime.date()
                        <= term.end_date
                    )
                ),
                None,
            )

            event_data = {
                "name": gcal_event.get("summary").strip(),
                "term": event_term,
                "description": gcal_event.get("description") or "",
            }

            if "late start" in event_data["name"].lower():
                event_data["name"] = "Late Start"

            if existing_event is not None:
                events_to_update.append(existing_event)
            else:
                event = Event(
                    gcal_id=gcal_id,
                    **event_data,
                    organization=school_org,
                    start_date=start_dtime,
                    end_date=end_dtime,
                    is_public=False,  # whitelist in admin
                    schedule_format="default",
                )
                events_to_create.append(event)

        except Exception:
            logger.warning(
                f"core.tasks.fetch_calendar_events: Failed to process event {gcal_event.get('id')}"
                + f"\n{traceback.format_exc()}"
            )

    from django.db import transaction

    if events_to_create:
        with transaction.atomic():
            # Event.objects.bulk_create(events_to_create, ignore_conflicts=True) # no logging? *megamind peeking*
            for event in events_to_create:
                try:
                    with transaction.atomic():
                        event.save()
                except Exception:
                    logger.exception(
                        f"Unexpected error while saving event '{event.name}' (id={event.id})"
                    )

    if events_to_update:
        with transaction.atomic():
            Event.objects.bulk_update(events_to_update, list(event_data.keys()))

    if events_to_delete:
        Event.objects.filter(id__in=[e.id for e in events_to_delete]).delete()

    events = events_to_create + events_to_update

    del existing_events
    del events_to_create
    del events_to_update
    del events_to_delete

    if len(events) == 0:
        return

    past_events = Event.objects.filter(
        end_date__lte=dt.datetime.now(dt.UTC) + dt.timedelta(days=-1)
    )[:100]

    data_for_llm = {
        "past_events": [],
        "available_tags": [tag.name for tag in Tag.objects.all()],
        "new_events": [],
        "available_schedule_formats": list(
            settings.TIMETABLE_FORMATS["2024-2025"]["schedules"].keys()
        ),
    }

    for past_event in past_events:
        tags = [tag.name for tag in past_event.tags.all()]
        name = past_event.name
        description = past_event.description

        data_for_llm["past_events"].append(
            {
                "event": name,
                "description": description,
                "tags": tags,
            }
        )

    for event in events:
        data_for_llm["new_events"].append(
            {"event": event.name, "description": event.description, "id": event.gcal_id}
        )

    prompt = f"You are a meticulous and organized secretary at a Canadian high school. Your job is to accurately categorize digital calendar events by placing tags on them. Accuracy and consistency are paramount. You will be provided an array of events below to be tagged. Each element in the array will contain the data for one event. The element will be in the format of a json object containing the name, description of the event as well as a id to identify the event. The available tags for tagging the events will be provided below to you in the format of an array (E.g. ['tag 1', 'tag 2', 'tag 3', ... ]). You are only allowed to use the provided tags to tag the events. {'' if data_for_llm['past_events'] == [] else 'To help with your job, you will be provided below with an array of past events that have already be properly tagged. Each element of the array will be in the format of a json object, containing the name, description and tags for the event. You can reference past events to help guide your decision process in tagging the new events. '}When outputting, output a single json object. The keys of the json object will match an id of an event that needed tagging and the value will be an array of all the tags relevant. Do not output anything besides the tags.\n\nAvailable Tags: {data_for_llm['available_tags']}\n{'' if data_for_llm['past_events'] == [] else 'Past events: ' + dumps(data_for_llm['past_events'])}\nEvents to be tagged: {dumps(data_for_llm['new_events'])}"

    try:
        response = prompt_gemini(prompt)
        response = response.text.replace("```json", "").replace("```", "")
        response = loads(response)

        tags = {}

    except Exception:
        logger.warning(traceback.format_exc())

    for event in events:
        try:
            for tag in response[event.gcal_id]:
                if tag not in tags:
                    tags[tag] = Tag.objects.filter(name__iexact=tag).first()

                    if tags[tag] is None:
                        logger.warning(f"Tag '{tag}' does not exist")
                        continue

                event.tags.add(tags[tag])

            event.save()
        except Exception:
            logger.warning(traceback.format_exc())

    prompt = f"You are a meticulous and organized secretary at a Canadian high school. Your job is to accurately set the start and ending time for events based on the information in the title or description of the event. In addition, you will also set the schedule format (E.g pa days, holidays, etc).  Accuracy and consistency are paramount. You will be provided an array of events below. Each element in the array will contain the data for one event. The element will be in the format of a json object containing the name, description of the event as well as a id to identify the event. The available schedule formats will be provided as an array below. You can only choose from the the array provided. All day will be referring to the entire school day (9:00 to 15:15). Holidays, P.A days, late starts and similar events will last all day. Periods are usually detailed in the name of the event (E.g. Period 1, Per 1, P1). Period 1 lasts from 9:00 to 10:20. Period 2 lasts from 10:25 to 11:40. Period 3 lasts from 12:40 to 13:55. Period 4 lasts from 14:00 to 15:15. The latest that any event finish at is 18:00 unless directly specified in the event. When outputting, output a single json object. The keys of the json object will match an id of an event that needs to have their time set and the value will be an array with three values, the starting, ending time and schedule format. Use 24h hour format for time, in the format of HH:MM. If the event title and description does not provide enough information to determine the starting or ending time, set both to be null. Default to default for the schedule format if you do not think any other schedule format is applicable. Do not output anything besides the tags.\nAvailable Schedule Formats: {data_for_llm['available_schedule_formats']} \nEvents: {dumps(data_for_llm['new_events'])}"

    try:
        response = prompt_gemini(prompt)

        response = response.text.replace("```json", "").replace("```", "")
        response = loads(response)

    except Exception:
        logger.warning(traceback.format_exc())

    for event in events:
        all_day_event = event.start_date == timezone.make_aware(
            dt.datetime.combine(
                dt.date.fromisoformat(gcal_start.get("date")),
                dt.time(0, 0),
            )
        ) and event.end_date == timezone.make_aware(
            dt.datetime.combine(
                dt.date.fromisoformat(gcal_end.get("date")),
                dt.time(23, 59),
            )
        )
        if not all_day_event:
            continue

        try:
            start_time, end_time, event_format = response[event.gcal_id]

            tz = timezone.get_current_timezone()

            if start_time is not None:
                start_time = dt.datetime.strptime(start_time, "%H:%M")
                event.start_date = event.start_date.astimezone(tz).replace(
                    hour=start_time.hour, minute=start_time.minute
                )
            if end_time is not None:
                end_time = dt.datetime.strptime(end_time, "%H:%M")
                event.end_date = event.end_date.astimezone(tz).replace(
                    hour=end_time.hour, minute=end_time.minute
                )

            event.schedule_format = event_format

            event.save()

        except Exception:
            logger.warning(traceback.format_exc())
