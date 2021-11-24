import datetime
import json
from dataclasses import dataclass

import rest_framework.utils.encoders
from django.shortcuts import reverse
from django.utils import timezone

from .. import models


@dataclass
class DaySchedule:
    schedule: dict
    is_personal: bool

    def get_schedule_nudge_message(info: WeekScheduleInfo) -> str:
        date = timezone.localdate()
        current_term = models.Term.get_current(target_date=date)
        if current_term is None:
            return None
        return info


@dataclass
class WeekScheduleInfo:
    json_data: str
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


def generic_day_schedule(term, date) -> DaySchedule:
    schedule = term.day_schedule(target_date=date) if term is not None else []
    # generic day schedule is personal if it is empty
    is_personal = len(schedule) == 0
    return DaySchedule(schedule, is_personal)


def get_day_schedule(user, target_date: datetime.datetime) -> DaySchedule:
    term = models.Term.get_current(target_date=target_date)
    personal_sch = DaySchedule(user.schedule(target_date=target_date), True)
    if not personal_sch.schedule:
        # generic schedule is more useful than an empty personal one
        return generic_day_schedule(term, target_date)
    return personal_sch


def get_week_schedule(user) -> dict:
    date = timezone.localdate()

    if user.is_authenticated:
        return {
            target_date.isoformat(): get_day_schedule(user, target_date)
            for target_date in [
                date + datetime.timedelta(days=days) for days in range(7)
            ]
        }
    return {
        target_date.isoformat(): generic_day_schedule(
            models.Term.get_current(target_date=target_date),
            target_date,
        )
        for target_date in [
            date + datetime.timedelta(days=days) for days in range(7)
        ]
    }


def get_week_schedule_info(user) -> WeekScheduleInfo:
    data = get_week_schedule(user)

    return WeekScheduleInfo(
        json_data=json.dumps(data, cls=JSONEncoder),
        nudge_add_timetable=not all(
            day_schedule.is_personal for day_schedule in data.values()
        ),
        logged_in=user.is_authenticated,
    )


