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


def get_week_schedule(user) -> dict:
    date = timezone.localdate()

    if user.is_authenticated:
        result = {}  # TODO: use a dictionary comprehension

        for day in range(7):
            term = models.Term.get_current(target_date=date)
            # first try using personal day schedule
            day_schedule = DaySchedule(user.schedule(target_date=date), True)
            # switch to generic day schedule if personal day schedule is empty
            if len(day_schedule.schedule) == 0:
                day_schedule = generic_day_schedule(term, date)
            result[date.isoformat()] = day_schedule
            date += datetime.timedelta(days=1)

        return result
    else:
        result = {}  # TODO: use a dictionary comprehension

        for day in range(7):
            term = models.Term.get_current(target_date=date)
            result[date.isoformat()] = generic_day_schedule(term, date)
            date += datetime.timedelta(days=1)
        return result


def get_week_schedule_info(user) -> WeekScheduleInfo:
    data = get_week_schedule(user)

    return WeekScheduleInfo(
        json_data=json.dumps(data, cls=JSONEncoder),
        nudge_add_timetable=not all(
            day_schedule.is_personal for day_schedule in data.values()
        ),
        logged_in=user.is_authenticated,
    )


def get_schedule_nudge_message(info: WeekScheduleInfo) -> str:
    date = timezone.localdate()
    current_term = models.Term.get_current(target_date=date)
    if current_term is None:
        return ""
    elif not info.logged_in:
        sign_up_url = reverse("account_signup")
        return f"<a href='{sign_up_url}'>Sign up</a> and add your timetable to see a personalized schedule here."
    elif info.nudge_add_timetable:
        add_timetable_url = reverse("timetable_create", args=[current_term.id])
        return f"<a href='{add_timetable_url}'>Add your timetable</a> to see a personalized schedule here."
    else:
        return ""
