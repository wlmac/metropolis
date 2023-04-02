import datetime

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models import Q
from django.utils import timezone
from multiselectfield import MultiSelectField

from .. import utils
from ..utils.utils import get_week_and_day


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
        return timezone.make_aware(
            datetime.datetime.combine(self.start_date, datetime.time())
        )

    def end_datetime(self):
        return timezone.make_aware(
            datetime.datetime.combine(
                self.end_date, datetime.time(hour=23, minute=59, second=59)
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
            cur_iter_day += datetime.timedelta(1)

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
                datetime.datetime.combine(target_date, datetime.time(*i["time"][0]))
            )
            end_time = timezone.make_aware(
                datetime.datetime.combine(target_date, datetime.time(*i["time"][1]))
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
    YEARLY - Repeat every year on the {event.start_date.strftime("%m%d")} day of the year with a {repeats_every} year interval.

    - TODO
    -  add in a way to cancel an event for a specific date / reschedule it.

    """

    class RecurrenceOptions(models.TextChoices):
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"
        YEARLY = "yearly"

    class DaySOfWeek(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    class MonthlyRepeatOptions(models.IntegerChoices):
        DATE = 0  # repeat on the first of that day (i.e. if the original event is on the 15th, the repeat will be on the 15th of the month)
        DAY = 1  # repeat on the first day of the month that matches the day of the week of the original event. e.g. if the original event is on the first tuesday, the repeat will be on the first tuesday of the month.

    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="reoccurrences"
    )
    type = models.CharField(
        max_length=16,
        choices=RecurrenceOptions.choices,
        help_text="the type of repetition. (e.g. daily, weekly, monthly, yearly)",
    )

    repeats_every = models.PositiveSmallIntegerField(
        default=1,
        help_text="repeats every x {type}. (e.g. 2 would mean every other day if type was DAILY)",
    )

    # --- repetition options ---
    repeat_on = MultiSelectField(
        choices=DaySOfWeek.choices,
        max_length=13,
        max_choices=7,
        blank=True,
        null=True,
        help_text="the days of the week to repeat on. or if type=MONTHLY, the first or last of x day to repeat on)",
    )
    # Used on weekly: the days of the week to repeat on e.g. 16 would be tuesday and sunday

    repeat_type = models.IntegerField(
        choices=MonthlyRepeatOptions.choices,
        help_text="the type of monthly repetition to use. (I.E. day, date)",
        blank=True,
        null=True,
    )

    # --- Custom ending options --- if neither of these are set, the event will repeat forever.
    ends = models.DateField(
        help_text="the date the repetition ends.", blank=True, null=True
    )
    ends_after = models.PositiveSmallIntegerField(
        help_text="the number of times to repeat the event before ending. e.g. 5 would mean the event will repeat 5 times before ending.",
        blank=True,
        null=True,
    )

    def _get_x_day_of_month(self, month, year):
        if self.repeat_type == self.MonthlyRepeatOptions.DATE:
            return self.event.start_date.day
        elif self.repeat_type == self.MonthlyRepeatOptions.DAY:
            first_day = datetime.date(year, month, 1)
            week, day = get_week_and_day(self.event.start_date)

            # Calculate the offset to the desired day of the week
            day_offset = (day - first_day.weekday()) % 7

            # Calculate the day of the month
            day_of_month = 1 + (week - 1) * 7 + day_offset

            # Combine the date and time to create a datetime object
            return datetime.datetime.combine(
                datetime.date(year, month, day_of_month), datetime.time.min
            )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(ends__isnull=True) | Q(ends_after__isnull=True),
                name="ends_or_ends_after",
            ),
            # This constraint ensures that either the ends or ends_after fields are set, but not both. This prevents conflicting data from being entered into the database.
            models.CheckConstraint(
                check=Q(type="weekly") | Q(repeat_on__isnull=True),
                name="repeat_on_only_with_weekly_type",
            ),
            # This constraint ensures that the repeat_on field is only set when the type is WEEKLY.
            models.CheckConstraint(
                check=models.Q(type="monthly") | models.Q(repeat_type__isnull=True),
                name="repeat_type_only_with_monthly_type",
            ),
            # This constraint ensures that the repeat_type field is only set when the type is MONTHLY.
            models.CheckConstraint(
                check=models.Q(type="daily", repeats_every__gt=1)
                | ~models.Q(type="daily"),
                name="daily_repeat_every_gt_1",
            ),
            # This constraint checks that the repeats_every field is greater than 1 when the type field is set to 'daily', and that the constraint is not applied when the type is not 'daily'.
        ]


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
