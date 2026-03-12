import datetime
import json
from dataclasses import dataclass

import rest_framework.utils.encoders
from django.utils import timezone
from django.utils.formats import time_format
from django.utils.safestring import SafeString, mark_safe

from .. import models


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


def generic_day_schedule(date=None, user=None) -> DaySchedule:
    return get_day_schedule(date, user, is_generic=True)


def get_period_datetimes(
    date, is_generic
) -> list[tuple[datetime.datetime, datetime.datetime]] | list:
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

        def t(h: int, m: int) -> datetime.time:
            return datetime.time(h, m)

        schedule_times = [
            (t(9, 0), t(10, 20)),
            (t(10, 25), t(11, 40)),
            (t(12, 40), t(13, 55)),
            (t(14, 0), t(15, 15)),
        ]

    if not is_generic:
        override = models.ScheduleOverride.objects.filter(date=date).first()

        is_weekend = date.weekday() >= 5
        is_summer = 7 <= date.month <= 8
        is_no_school_override = (
            override and override.pattern.p1_start == override.pattern.p4_end
        )

        if any(
            [
                is_weekend,
                is_summer,
                is_no_school_override,
            ]
        ):
            schedule_times = []
        elif override:
            pattern = override.pattern
            schedule_times = [
                (
                    getattr(pattern, f"p{i + 1}_start"),
                    getattr(pattern, f"p{i + 1}_end"),
                )
                for i in range(4)
            ]

    def dt(d: datetime.date, t: datetime.time) -> datetime.datetime:
        return timezone.make_aware(datetime.datetime.combine(d, t))

    schedule_datetimes = [
        (dt(date, p_start), dt(date, p_end)) for (p_start, p_end) in schedule_times
    ]

    return schedule_datetimes


def get_day_schedule(date=None, user=None, is_generic=False) -> DaySchedule:
    date = date or timezone.localdate()

    schedule_times = get_period_datetimes(date, is_generic)

    if not schedule_times:
        return {"schedule": [], "cycle": 0, "is_personal": True}

    is_personal = (
        user is not None and user.is_authenticated and hasattr(user, "timetable")
    )

    courses = user.timetable.get_courses_as_dict() if is_personal else {}

    return {
        "cycle": 1 if date.day % 2 == 1 else 2,
        "is_personal": is_personal,
        "schedule": [
            {
                "description": {
                    "time": f"{time_format(period_start, 'g:i A')} - {time_format(period_end, 'g:i A')}",
                    "course": courses.get(period_num, {}).get("name")
                    or f"Period {period_num}",
                    "room": courses.get(period_num, {}).get("room") or "",
                    "teacher": courses.get(period_num, {}).get("teacher") or "",
                },
                "time": {
                    "start": period_start,
                    "end": period_end,
                },
            }
            for period_num, (period_start, period_end) in zip(
                [1, 2, 4, 3] if date.day % 2 == 0 else [1, 2, 3, 4],
                schedule_times,
                strict=False,
            )
        ],
    }


def get_week_schedule(date=None, user=None) -> dict:
    date = date or timezone.localdate()
    return {
        target_date.isoformat(): get_day_schedule(target_date, user)
        for target_date in [date + datetime.timedelta(days=days) for days in range(7)]
    }


def get_week_schedule_info(user) -> WeekScheduleInfo:
    data = get_week_schedule(date=None, user=user)
    return WeekScheduleInfo(
        json_data=mark_safe(json.dumps(data, cls=JSONEncoder)),
        nudge_add_timetable=not all(
            day_schedule.get("is_personal") for day_schedule in data.values()
        ),
        logged_in=user.is_authenticated,
    )
