import datetime
import json
from dataclasses import dataclass

import rest_framework.utils.encoders
from django.utils import timezone
from django.utils.formats import time_format
from django.utils.safestring import SafeString, mark_safe

from .. import models
from .local_date import get_localdate


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


class JSONEncoder(rest_framework.utils.encoders.JSONEncoder):
    """
    Extends rest_framework JSONEncoder to encode DaySchedule.
    """

    def default(self, obj):
        if isinstance(obj, DaySchedule):
            return obj.__dict__
        return super().default(obj)


def generic_day_schedule(date=None, user=None):
    return get_day_schedule(date, user, generic=True)


def get_day_schedule(date=None, user=None, generic=False) -> DaySchedule:
    date = get_localdate(date)
    tz = timezone.get_current_timezone()

    default_pattern = models.SchedulePattern.objects.filter(
        name__iexact="Default"
    ).first()

    if default_pattern:
        schedule_times = [
            (
                getattr(default_pattern, f"p{i + 1}_start"),
                getattr(default_pattern, f"p{i + 1}_end"),
            )
            for i in range(4)
        ]
    else:

        def t(h, m):
            return datetime.datetime.combine(date, datetime.time(h, m, tzinfo=tz))

        schedule_times = [
            (t(9, 0), t(10, 20)),
            (t(10, 25), t(11, 40)),
            (t(12, 40), t(13, 55)),
            (t(14, 0), t(15, 15)),
        ]

    if not generic:
        override = models.ScheduleOverride.objects.filter(date=date).first()

        if override:
            schedule_times = [
                (
                    getattr(override.pattern, f"p{i + 1}_start"),
                    getattr(override.pattern, f"p{i + 1}_end"),
                )
                for i in range(4)
            ]
        elif date.weekday() >= 5 or 7 <= date.month <= 8:
            return {"schedule": [], "cycle": 0, "is_personal": True}

    is_personal = (
        user is not None and user.is_authenticated and hasattr(user, "timetable")
    )

    if is_personal:
        courses = user.timetable.get_courses_as_dict()

    return {
        "cycle": 1 if date.day % 2 == 1 else 2,
        "is_personal": is_personal,
        "schedule": [
            {
                "description": {
                    "time": f"{time_format(period_start, 'g:i A')} - {time_format(period_end, 'g:i A')}",
                    "course": f"Period {period_num}"
                    if not is_personal
                    else courses.get(period_num, {}).get("name")
                    or f"Period {period_num}",
                },
                "time": {
                    "start": period_start,
                    "end": period_end,
                },
            }
            for i, period_num, (period_start, period_end) in zip(
                range(4),
                [1, 2, 4, 3] if date.weekday() % 2 == 0 else [1, 2, 3, 4],
                schedule_times,
            )
        ],
    }


def get_week_schedule(user) -> dict:
    date = timezone.localdate()
    return {
        target_date.isoformat(): get_day_schedule(date, user)
        for target_date in [date + datetime.timedelta(days=days) for days in range(7)]
    }


def get_week_schedule_info(user) -> WeekScheduleInfo:
    data = get_week_schedule(user)
    return WeekScheduleInfo(
        json_data=mark_safe(json.dumps(data, cls=JSONEncoder)),
        nudge_add_timetable=not all(
            day_schedule.get("is_personal") for day_schedule in data.values()
        ),
        logged_in=user.is_authenticated,
    )
