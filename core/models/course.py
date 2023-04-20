from __future__ import annotations

import datetime as dt
from typing import List

from dateutil.rrule import rrule, MONTHLY, WEEKLY, DAILY, YEARLY
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

from .. import utils
from ..utils.fields import PositiveOneSmallIntegerField
from ..utils.utils import *


class Term(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    timetable_format = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    is_frozen = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def start_datetime(self):
        return timezone.make_aware(dt.datetime.combine(self.start_date, dt.time()))

    def end_datetime(self):
        return timezone.make_aware(
            dt.datetime.combine(
                self.end_date, dt.time(hour=23, minute=59, second=59)
            )
        )

    def is_current(self, target_date=None):
        target_date = utils.get_localdate(date=target_date)
        return self.start_date <= target_date < self.end_date

    def day_is_instructional(self, target_date=None):
        target_date = utils.get_localdate(date=target_date, time=[11, 0, 0])
        return (
            target_date.weekday() < 5
            and not self.events.filter(
                is_instructional=False,
                start_date__lte=target_date,
                end_date__gte=target_date,
            ).exists()
        )

    def day_num(self, target_date=None):
        tf = settings.TIMETABLE_FORMATS[self.timetable_format]
        methods = {
            "consecutive": self.__day_num_consecutive,
            "calendar_days": self.__day_num_calendar_days,
        }
        target_date = utils.get_localdate(date=target_date, time=[23, 59, 59])
        if not self.is_current(target_date.date()) or not self.day_is_instructional(
            target_date
        ):
            return None
        return methods[tf.get("day_num_method", "consecutive")](tf, target_date)

    @staticmethod
    def __day_num_calendar_days(tf, target_date):
        """
        Gets the day number from if the calendar day is even (day 2) or odd (day 1).
        """
        if tf["cycle"]["length"] != 2:
            raise TypeError(
                "calendar_days cannot be used in formats where cycle length != 2"
            )
        even, odd = 0, 1
        return {even: 2, odd: 1}[target_date.day % 2]

    def __day_num_consecutive(self, tf, target_date):
        """
        Gets the day number by counting consecutive days.
        """
        cycle_duration = tf["cycle"]["duration"]

        cur_iter_day = self.start_datetime().replace(hour=11, minute=0, second=0)
        cycle_day_type_set = set()

        while cur_iter_day <= target_date:
            if self.day_is_instructional(cur_iter_day):
                if cycle_duration == "day":
                    cycle_day_type_set.add(cur_iter_day.timetuple().tm_yday)
                elif cycle_duration == "week":
                    cycle_day_type_set.add(cur_iter_day.isocalendar()[1])
                else:
                    raise NotImplementedError
            cur_iter_day += dt.timedelta(1)

        return (len(cycle_day_type_set) - 1) % tf["cycle"]["length"] + 1

    def day_schedule_format(self, target_date=None):
        tds = utils.get_localdate(date=target_date, time=[0, 0, 0])  # target date start
        tde = utils.get_localdate(
            date=target_date, time=[23, 59, 59]
        )  # target date end

        schedule_formats = settings.TIMETABLE_FORMATS[self.timetable_format][
            "schedules"
        ]
        schedule_format_set = set(
            self.events.filter(start_date__lte=tde, end_date__gte=tds).values_list(
                "schedule_format", flat=True
            )
        ).intersection(set(schedule_formats.keys()))
        for schedule_format in list(schedule_formats.keys())[::-1]:
            if schedule_format in schedule_format_set:
                return schedule_format

        return "default"

    def day_schedule(self, target_date=None):
        target_date = utils.get_localdate(date=target_date)

        timetable_config = settings.TIMETABLE_FORMATS[self.timetable_format]
        day_num = self.day_num(target_date=target_date)

        if day_num is None:
            return []

        result = []

        for i in timetable_config["schedules"][
            self.day_schedule_format(target_date=target_date)
        ]:
            start_time = timezone.make_aware(
                dt.datetime.combine(target_date, dt.time(*i["time"][0]))
            )
            end_time = timezone.make_aware(
                dt.datetime.combine(target_date, dt.time(*i["time"][1]))
            )

            result.append(
                {
                    "description": i["description"],
                    "time": {
                        "start": start_time,
                        "end": end_time,
                    },
                    "position": i["position"][day_num - 1],
                    "cycle": f'{timetable_config["cycle"]["duration"].title()} {day_num}',
                    "course": f'{timetable_config["cycle"]["duration"].title()} {day_num} {i["description"]["course"]}',
                }
            )

        return result

    class MisconfiguredTermError(Exception):
        pass

    @classmethod
    def get_current(cls, target_date=None):
        target_date = utils.get_localdate(date=target_date)

        try:
            return cls.objects.get(
                start_date__lte=target_date, end_date__gt=target_date
            )
        except cls.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            raise cls.MisconfiguredTermError


class Course(models.Model):
    code = models.CharField(max_length=16)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="courses")
    description = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField()

    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code", "term"], name="unique_course"),
        ]


class RecurrenceRule(models.Model):
    """
    Recurrence rules for events.

    DAILY - Repeats daily with a {repeats_every} day interval.
    WEEKLY - Repeats weekly on {repeat_on} days with a {repeats_every} week interval
    MONTHLY - Repeat every month on the {event.start_date.strftime("%d")} day of the month or {get_week_and_day(event.start_date)} (for example this could be the 2nd tuesday of the month) with a {repeats_every} month interval.
            Date - repeat on the first of that day (i.e. if the original event is on the 15th, the repeat will be on the 15th of the month)
            Day  - repeat on the first day of the month that matches the day of the week of the original event. e.g. if the original event is on the first tuesday, the repeat will be on the first tuesday of the month.
    YEARLY - Repeat every year on the {event.start_date.strftime("%m%d")} day of the year with a {repeats_every} year interval.

    - TODO
    -  add in a way to cancel an event for a specific date / reschedule it.

    """

    class RecurrenceOptions(models.IntegerChoices):
        DAILY = DAILY
        WEEKLY = WEEKLY
        MONTHLY = MONTHLY
        YEARLY = YEARLY

    class DaysOfWeek(models.IntegerChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    class MonthlyRepeatOptions(models.IntegerChoices):
        DATE = 0  # repeat on the first of that day (i.e. if the original event is on the 15th, the repeat will be on the 15th of the month)
        DAY = 1  # repeat on the first day of the month that matches the day of the week of the original event. e.g. if the original event is on the first tuesday, the repeat will be on the first tuesday of the month.

    class MonthsOfYear(models.IntegerChoices):
        JANUARY = 1
        FEBRUARY = 2
        MARCH = 3
        APRIL = 4
        MAY = 5
        JUNE = 6
        JULY = 7
        AUGUST = 8
        SEPTEMBER = 9
        OCTOBER = 10
        NOVEMBER = 11
        DECEMBER = 12

    event = models.OneToOneField(
        "Event",
        on_delete=models.CASCADE,
        related_name="reoccurrences",
        related_query_name="reoccurrence",
        unique=True,
    )
    type = models.IntegerField(
        choices=RecurrenceOptions.choices,
        help_text="the type of repetition. (e.g. daily, weekly, monthly, yearly)",
    )

    interval = PositiveOneSmallIntegerField(
        default=1,
        help_text="The interval between each freq iteration. For example, when using YEARLY, an interval of 2 means once every two years, but with HOURLY, it means once every two hours. The default interval is 1.",
    )

    # --- repetition options ---
    repeat_on = MultiSelectField(
        choices=DaysOfWeek.choices,
        blank=True,
        null=True,
        help_text="the days of the week to repeat on. or if type=MONTHLY, the first or last of x day to repeat on)",
    )
    # Used on weekly: the days of the week to repeat on e.g. 16 would be tuesday and sunday

    repeat_type = models.IntegerField(  # fixme - not used in rrule
        choices=MonthlyRepeatOptions.choices,
        help_text="the type of monthly repetition to use. (I.E. day, date)",
        blank=True,
        null=True,
    )
    repeat_months = MultiSelectField(
        choices=MonthsOfYear.choices,
        help_text="If given, it must be either an month, or a sequence of months, meaning the months to apply the recurrence to. (only allowed for monthly and yearly recurrences)",
        blank=True,
        null=True,
    )
    repeat_monthdays = MultiSelectField(
        help_text="If given, it must be either an integer, or a sequence of integers, meaning the days of the month to apply the recurrence to. (only allowed for monthly and yearly recurrences)",
        choices=[(i, i) for i in range(1, 32)],
        blank=True,
        null=True,
    )

    # --- Custom ending options --- if neither of these are set, the recurrences will repeat forever.
    ends = models.DateField(
        help_text="the date the repetition ends.", blank=True, null=True
    )
    ends_after = PositiveOneSmallIntegerField(
        help_text="the number of times to repeat the event before ending. e.g. 5 would mean the event will reoccur 5 times before stopping.",
        blank=True,
        null=True,
    )

    @property
    def _repeat_on(self):
        return tuple(map(int, self.repeat_on))

    def clean(self):
        if self.ends is not None and self.ends_after is not None:
            raise ValidationError(
                "You can set ends or ends_after, or neither but not both."
            )
        if self.repeat_type is not None:
            if self.type != self.RecurrenceOptions.MONTHLY:
                raise ValidationError(
                    "You can only set repeat_type if the type is MONTHLY."
                )

        if self.type not in [
            self.RecurrenceOptions.WEEKLY,
            self.RecurrenceOptions.MONTHLY,
        ]:
            if self.repeat_on:
                raise ValidationError(
                    "You can only set repeat_on if the type is WEEKLY or MONTHLY."
                )
        if self.repeat_monthdays:
            for month in self.repeat_months:
                if self.repeat_monthdays < daysPerMonth[month]:
                    raise ValidationError(
                        f"Month {month} does not have a day {self.repeat_monthdays}, it only has {daysPerMonth[month]} days."
                    )

        return super().clean()

    @property
    def get_repeat_months(self) -> None | List[int] | int:
        """Returns the repeat_months as a list of ints (instead of list of str) or None if it's not set."""
        if self.repeat_months:
            return (
                [int(day) for day in self.repeat_months]
                if type(self.repeat_months) == list
                else int(self.repeat_months[0])
            )
        return None

    @property
    def get_repeat_monthdays(self) -> None | List[int] | int:
        """Returns the repeat_monthdays as a list of ints (instead of list of str) or None if it's not set."""
        if self.repeat_monthdays:
            return (
                [int(day) for day in self.repeat_monthdays]
                if type(self.repeat_monthdays) == list
                else int(self.repeat_monthdays[0])
            )
        return None

    @property
    def rule(self):
        rule = rrule(
            freq=self.type,
            dtstart=self.event.start_date,
            interval=self.interval,
            wkst=None,  # todo add weekstart
            until=self.ends,
            count=self.ends_after,
            bysetpos=None,
            bymonth=self.get_repeat_months,
            bymonthday=self.get_repeat_monthdays,
            # byweekno=None,, maybe impl later on (used for when you want to schedule events every x weeks)
            byweekday=self._repeat_on,
            cache=True,
        )
        print(rule.__str__())
        return rule

    def _get_x_day_of_month(self) -> dt.date:
        if self.repeat_type == self.MonthlyRepeatOptions.DATE:
            return self.event.start_date.day
        elif self.repeat_type == self.MonthlyRepeatOptions.DAY:
            first_day = dt.date(
                self.event.start_date.year, self.event.start_date.month, 1
            )
            week, day = get_week_and_day(self.event.start_date)

            # Calculate the offset to the desired day of the week
            day_offset = (day - first_day.weekday()) % 7

            # Calculate the day of the month
            day_of_month = 1 + (week - 1) * 7 + day_offset

            # Combine the date and time to create a datetime object
            return dt.datetime.combine(
                dt.date(
                    self.event.start_date.year,
                    self.event.start_date.month,
                    day_of_month,
                ),
                dt.time.min,
            )


class Event(models.Model):
    name = models.CharField(max_length=64)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="events")

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="events",
        related_query_name="event",
    )
    description = models.TextField(blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    schedule_format = models.CharField(max_length=64, default="default")
    is_instructional = models.BooleanField(
        default=True,
        help_text="Whether school instruction is taking place during this event. Leave checked if not direct cause.",
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether if this event pertains to the general school population, not just those in the organization.",
    )
    should_announce = models.BooleanField(
        default=False,
        help_text="Whether if this event should be announced to the general school population VIA the important events feed.",
    )

    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="events", related_query_name="event"
    )

    def __str__(self):
        return self.name

    def is_current(self):
        today = timezone.localtime()
        return self.start_date <= today < self.end_date

    @classmethod
    def get_events(cls, user=None):
        events = cls.objects.filter(is_public=True)
        if user is not None and user.is_authenticated:
            events = (events | events.filter(organization__member=user)).distinct()

        return events
