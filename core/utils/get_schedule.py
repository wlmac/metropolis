import datetime
import json
from dataclasses import dataclass

import rest_framework.utils.encoders
from django.utils import timezone
from django.utils.safestring import SafeString, mark_safe

from .. import models


# TODO remove
@dataclass
class DaySchedule:
    schedule: dict
    cycle: int
    is_personal: bool


@dataclass
class WeekScheduleInfo:
    json_data: SafeString
    logged_in: bool
    nudge_add_timetable: bool
    # current_term_id: int


class JSONEncoder(rest_framework.utils.encoders.JSONEncoder):
    """
    Extends rest_framework JSONEncoder to encode DaySchedule.
    """

    def default(self, obj):
        if isinstance(obj, DaySchedule):
            return obj.__dict__
        return super().default(obj)


# def generic_day_schedule(term, date) -> DaySchedule:
#     schedule = term.day_schedule(target_date=date) if term is not None else []
#     # generic day schedule is personal if it is empty
#     is_personal = len(schedule) == 0
#     return DaySchedule(schedule, is_personal)


# def get_day_schedule(user, target_date: datetime.datetime) -> DaySchedule:
#     term = models.Term.get_current(target_date=target_date)
#     personal_sch = DaySchedule(user.schedule(target_date=target_date), True)
#     if not personal_sch.schedule:
#         # generic schedule is more useful than an empty personal one
#         return generic_day_schedule(term, target_date)
#     return personal_sch


def get_day_schedule(date, user):
    if date.weekday() >= 5 or 7 <= date.month <= 8:
        return {"schedule": [], "cycle": 0, "is_personal": True}

    tz = timezone.get_current_timezone()

    def t(h, m):
        return datetime.datetime.combine(date, datetime.time(h, m, tzinfo=tz))

    schedule = [
        (t(9, 0), t(10, 20)),
        (t(10, 25), t(11, 40)),
        (t(12, 40), t(13, 55)),
        (t(14, 0), t(15, 15)),
    ]

    override = (
        models.ScheduleOverride.objects.filter(date=date)
        .select_related("pattern")
        .first()
    )
    if override:
        pattern = override.pattern.as_dict()
        schedule = [
            (
                pattern.get(f"p{i + 1}_start"),
                pattern.get(f"p{i + 1}_end"),
            )
            for i in range(4)
        ]

    is_personal = user.is_authenticated  # TODO: and user's personal schedule exists

    return {
        "cycle": 1 if date.day % 2 == 1 else 2,
        "is_personal": is_personal,
        "schedule": [
            {
                "description": {
                    "time": f"{period_start.strftime('%I:%M %p')} - {period_end.strftime('%I:%M %p')}",
                    "course": f"Period {i + 1}"
                    if not is_personal
                    else "something",  # TODO
                },
                "time": {
                    "start": period_start,
                    "end": period_end,
                },
                "order": i + 1,
            }
            for i, (period_start, period_end) in enumerate(schedule)
        ],
    }


def get_week_schedule(user) -> dict:
    date = timezone.localdate()
    return {
        target_date.isoformat(): get_day_schedule(target_date, user)
        for target_date in [date + datetime.timedelta(days=days) for days in range(7)]
    }


# def get_week_schedule(user) -> dict:
#     date = timezone.localdate()

#     if user.is_authenticated:
#         return {
#             target_date.isoformat(): get_day_schedule(user, target_date)
#             for target_date in [
#                 date + datetime.timedelta(days=days) for days in range(7)
#             ]
#         }
#     return {
#         target_date.isoformat(): generic_day_schedule(
#             models.Term.get_current(target_date=target_date),
#             target_date,
#         )
#         for target_date in [date + datetime.timedelta(days=days) for days in range(7)]
#     }


def get_week_schedule_info(user) -> WeekScheduleInfo:
    data = get_week_schedule(user)
    # current_term = models.Term.get_current()
    return WeekScheduleInfo(
        json_data=mark_safe(json.dumps(data, cls=JSONEncoder)),
        nudge_add_timetable=not all(
            day_schedule.get("is_personal") for day_schedule in data.values()
        ),
        logged_in=user.is_authenticated,
        # current_term_id=current_term.id if current_term else None,
    )
