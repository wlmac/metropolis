import datetime as dt
import functools
from json import dumps, loads
from pathlib import Path

import gspread
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
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

from core.models import (
    Announcement,
    BlogPost,
    Event,
    Organization,
    Tag,
    User,
)
from core.utils.ai import prompt_gemini
from core.utils.tasks import get_random_username
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

    sender.add_periodic_task(
        crontab(hour=8, minute=30, day_of_week="mon-fri"), fetch_announcements
    )

    # sender.add_periodic_task(crontab(hour=4, minute=0), fetch_calendar_events)


@app.task
def delete_expired_users():
    """Scrub user data from inactive accounts that have not logged in for 14 days. (marked deleted)"""
    queryset = User.objects.filter(
        is_deleted=True,
        last_login__lt=timezone.make_aware(dt.datetime.now() - dt.timedelta(days=14)),
    )
    for user in queryset:
        user.organizations.clear()
    queryset.update(  # We need to object to not break posts or comments
        first_name="Deleted",
        last_name="User",
        username=get_random_username(),
        bio="",
        # timezone="",
        graduating_year=None,
        is_teacher=False,
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
            if isinstance(allowlist, dict) and msg_kwargs["category"] not in allowlist:
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
            raise self.retry(exc=exc) from exc
        try:
            resp.validate_response()
        except DeviceNotRegisteredError:
            notreg_tokens.add(token)
        except PushTicketError as exc:
            raise self.retry(exc=exc) from exc
    if notreg_tokens:
        u = User.objects.filter(id=recipient_id).first()
        for token in notreg_tokens:
            del u.expo_notif_tokens[token]
        u.save()


@app.task
def oauth2_clear_expired():
    from oauth2_provider.models import clear_expired

    clear_expired()


@app.task
def fetch_announcements():
    import traceback

    if settings.GOOGLE_SHEET_ID == "" or settings.GOOGLE_SHEET_ID is None:
        logger.warning("Fetch Announcements: GOOGLE_SHEET_ID is empty")
        return

    SERVICE_PATH = settings.SECRETS_PATH + "/service_account.json"

    if not Path(SERVICE_PATH).is_file():
        logger.warning(f"Fetch Announcements: {SERVICE_PATH} does not exist")
        return

    client = gspread.service_account(filename=SERVICE_PATH)
    worksheet = None

    try:
        worksheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
    except Exception:
        logger.warning("Fetch Announcements: Failed to open google sheet")
        return

    row_counter = 1

    """

    all_announcement_data -> List of dicts where every element is a row scraped from the spreadsheet
        Current Format Of Each Element:
            {
                "author": <User object>,
                "body": A string with the content of the announcement,
                "club_name": A string with the club name scraped from the google sheet,
                "show_after" A datetime that is timezone aware of when to display the announcement,
                "status": 'a' (For auto approving the announcement)
            }
    row_values -> List of strings containing the value of one row of the spreadsheet
        Current Format Of List (Matches the Google Sheet):
            Index 0: Timestamp (of when the form was submitted)
            Index 1: Email Address (of the person submitting it)
            Index 2: Date (of when the form was submitted)
            Index 3: Student Name (of the student who submitted the form)
            Index 4: Staff Advisor (of the club)
            Index 5: Club (club name)
            Index 6: Start Date (of when the announcement should be read)
            Index 7: End Date (of the last date the announcement should be read)
            Index 8: Announcement (the announcement to be read)

    """

    all_announcement_data = []

    while True:
        row_values = []

        try:
            row_values = [value.strip() for value in worksheet.row_values(row_counter)]
        except Exception:
            logger.warning(f"Fetch Announcements: Failed to read row {row_counter}")
            break

        if row_counter == 1:
            if row_values != [
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
                return
        else:
            if row_values == []:
                break
            else:
                try:
                    parsed_data = {
                        "body": row_values[8],
                        "club_name": row_values[5],
                        "status": "a",
                    }

                    # No point in including the author since it's an automated process
                    # author = User.objects.filter(email=row_values[1]).first()
                    # parsed_data["author"] = author

                    show_after = timezone.make_aware(
                        dt.datetime.strptime(row_values[6], "%m/%d/%Y")
                    ) + dt.timedelta(
                        hours=timezone.now()
                        .astimezone(timezone.get_current_timezone())
                        .hour
                    )
                    parsed_data["show_after"] = show_after

                    if show_after <= timezone.now() < show_after + dt.timedelta(days=1):
                        all_announcement_data.append(parsed_data)

                except Exception:
                    logger.warning(
                        f"Fetch Announcements: Failed to parse row {row_counter}"
                        + f"\n{traceback.format_exc()}"
                    )

        row_counter += 1

    prompt_data = []

    organizations_dict = {
        organization.name: {
            "execs": set(organization.execs.all()),
            "supervisors": set(organization.supervisors.all()),
            "organization": organization,
        }
        for organization in Organization.objects.filter(
            is_active=True
        ).prefetch_related("execs", "supervisors")
    }

    organizations = list(organizations_dict.keys())

    for parsed in all_announcement_data:
        prompt_data.append({"body": parsed["body"], "club_name": parsed["club_name"]})

    prompt = f"You are a meticulous and organized secretary at a Canadian high school. Your job is to accurately assign titles to announcements and figure out which club that announcement belongs to. Accuracy and consistency are paramount. The titles should be no more than 64 characters long. It should be descriptive of the announcement itself. Do not go over the limit. You will be provided an array of announcements. Each element in the array will contain the data for one announcement. The element will be in the format of a json object containing the body (what will be announced out) and the club_name (students may mistype clubs names, etc so you will need to pick which one you think they were trying to reference). The available names of all the clubs of the school will be provided below to you in the format of an array (E.g. ['club name 1', 'club name 2', 'club name 3', ... ]). \nWhen outputting, output a single array object. The array order must match the order of the one provided to you. DO NOT CHANGE THE ORDER UNDER ANY CIRCUMSTANCE. The array format should be the same as announcements array given to you. Each element are to be a json object, one key will be the title and the other will be the club name. Should no club match the one the student was trying to pick, then and ONLY then will you put down the club name they have listed. In this scenario, please output it in pascal case and remove any unnecessary information that is not relating to the club name itself. For example, if it's written as 'CLUB NAME (OTHER INFORMATION)', it should be outputted as just 'Club Name'. If you do find a club name in the club name array that matches the one the student was trying to write, it should be EXACTLY the same during output. Do not output anything besides the array.\nClub names: {organizations}\nAnnouncements to be titled: {dumps(prompt_data)}"
    for _ in range(3):
        try:
            response = prompt_gemini(prompt, model="models/gemini-2.5-flash")
            response = response.text.replace("```json", "").replace("```", "")
            response = loads(response)

            assert isinstance(response, list) and all(
                isinstance(item, dict)
                and "title" in item
                and "club_name" in item
                and isinstance(item["title"], str)
                and isinstance(item["club_name"], str)
                for item in response
            )

            break
        except Exception:
            response = None

    if response is None:
        logger.warning("Fetch Announcements: Failed to get response from Gemini")
        return

    for index, el in enumerate(response):
        try:
            announcement_data = all_announcement_data[index]

            try:
                org_details = organizations_dict[el["club_name"]]
                announcement_data["organization"] = org_details["organization"]

                if announcement_data["author"] is not None and not (
                    announcement_data["author"] in org_details["execs"]
                    or announcement_data["author"] in org_details["supervisors"]
                ):
                    announcement_data["author"] = None
            except KeyError:
                announcement_data["organization_string"] = el["club_name"]

            announcement_data["title"] = el["title"]
            del announcement_data["club_name"]

            Announcement.objects.get_or_create(
                body=announcement_data["body"], defaults=announcement_data
            )
        except Exception:
            logger.warning(
                f"Fetch Announcements: Failed to create announcement for row {index + 2}"
                + f"\n{traceback.format_exc()}"
            )


@app.task
def fetch_calendar_events():
    import traceback

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
    if settings.DEBUG:
        print(response.status_code)

    if response.status_code != 200:
        raise Exception(
            f"{str(response.status_code)} - Failed to fetch calendar events"
        )

    gcal_eventlist = response.json().get("items", [])
    if settings.DEBUG:
        print(len(gcal_eventlist), gcal_eventlist)

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

    events = []
    for gcal_event in gcal_eventlist:
        if (gcal_event.get("summary") or "").strip().lower() in ["day 1", "day 2"]:
            continue

        try:
            gcal_id = gcal_event.get("id")
            status = gcal_event.get("status")
            existing_event = existing_events.get(gcal_id)

            if existing_event is not None and (status is None or status == "cancelled"):
                existing_event.delete()
                continue

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

            event_data = {
                "name": (gcal_event.get("summary") or "").strip(),
                "description": gcal_event.get("description") or "",
                "start_date": start_dtime,
                "end_date": end_dtime,
            }

            if "late start" in event_data["name"].lower():
                event_data["name"] = "Late Start"

            if existing_event is not None:
                if all(
                    [
                        existing_event.name == event_data["name"],
                        existing_event.description == event_data["description"],
                        existing_event.start_date.astimezone().date()
                        == event_data["start_date"].date(),
                        existing_event.end_date.astimezone().date()
                        == event_data["end_date"].date(),
                    ]
                ):
                    continue

                try:
                    for key, value in event_data.items():
                        setattr(existing_event, key, value)

                    existing_event.save()
                    events.append(existing_event)
                except Exception:
                    logger.exception(
                        f"Unexpected error while updating event '{existing_event.name}' (id={existing_event.id})"
                    )
            else:
                event = Event(
                    gcal_id=gcal_id,
                    **event_data,
                    organization=school_org,
                    is_public=False,  # whitelist in admin
                    schedule_format="default",
                )

                try:
                    event.save()
                    events.append(event)
                except Exception:
                    logger.exception(
                        f"Unexpected error while saving event '{event.name}' (id={event.id})"
                    )

        except Exception:
            logger.warning(
                f"core.tasks.fetch_calendar_events: Failed to process event {gcal_event.get('id')}"
                + f"\n{traceback.format_exc()}"
            )

    if len(events) == 0:
        return

    past_events = Event.objects.filter(
        end_date__lte=dt.datetime.now(dt.UTC) + dt.timedelta(days=-1)
    )[:100]

    data_for_llm = {
        "past_events": [],
        "available_tags": [tag.name for tag in Tag.objects.all()],
        "new_events": [],
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

    for _ in range(3):
        try:
            response = prompt_gemini(prompt)
            response = response.text.replace("```json", "").replace("```", "")
            response = loads(response)
        except Exception:
            response = None

    if response is None:
        logger.warning(traceback.format_exc())
    else:
        tags = {}
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

    prompt = f"You are a meticulous and organized secretary at a Canadian high school. Your job is to accurately set the start and ending time for events based on the information in the title or description of the event.  Accuracy and consistency are paramount. You will be provided an array of events below. Each element in the array will contain the data for one event. The element will be in the format of a json object containing the name, description of the event as well as a id to identify the event. When outputting, output a single json object. The keys of the json object will match an id of an event that needs to have their time set and the value will be an array with three values, the starting, ending time and schedule format. Use 24h hour format for time, in the format of HH:MM. If the event title and description does not provide enough information to determine the starting or ending time, set both to be null. Default to default for the schedule format if you do not think any other schedule format is applicable. Do not output anything besides the tags. \nEvents: {dumps(data_for_llm['new_events'])}"

    for _ in range(3):
        try:
            response = prompt_gemini(prompt)
            response = response.text.replace("```json", "").replace("```", "")
            response = loads(response)
        except Exception:
            response = None

    if response is None:
        logger.warning(traceback.format_exc())
    else:
        for event in events:
            try:
                start_time, end_time, event_format = response[event.gcal_id]

                if start_time is not None:
                    start_time = dt.datetime.strptime(start_time, "%H:%M")
                    event.start_date = event.start_date.astimezone().replace(
                        hour=start_time.hour, minute=start_time.minute
                    )
                if end_time is not None:
                    end_time = dt.datetime.strptime(end_time, "%H:%M")
                    event.end_date = event.end_date.astimezone().replace(
                        hour=end_time.hour, minute=end_time.minute
                    )

                event.save()
            except Exception:
                logger.warning(traceback.format_exc())
