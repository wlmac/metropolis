from django.db import models
from django.urls import reverse
from metropolis import settings
from django.utils import timezone
import datetime
from metropolis import settings

# Create your models here.


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
        return timezone.make_aware(datetime.datetime.combine(self.start_date, datetime.time()))

    def end_datetime(self):
        return timezone.make_aware(datetime.datetime.combine(self.end_date, datetime.time(hour=23, minute=59, second=59)))

    def is_ongoing(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()
        return target_date >= self.start_date and target_date < self.end_date

    def day_is_instructional(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()
        target_date = timezone.make_aware(datetime.datetime.combine(target_date, datetime.time(hour=11, minute=00, second=00)))

        return target_date.weekday() < 5 and not self.events.filter(is_instructional=False, start_date__lte=target_date, end_date__gte=target_date).exists()

    def day_num(self, target_date=None):
        cycle_duration = settings.TIMETABLE_FORMATS[self.timetable_format]['cycle']['duration']

        if target_date == None:
            target_date = timezone.localdate()
        target_date = timezone.make_aware(datetime.datetime.combine(target_date, datetime.time(hour=23, minute=59, second=59)))

        cur_iter_day = self.start_datetime().replace(hour=11, minute=0, second=0)
        cycle_day_type_set = set()

        if not self.is_ongoing(target_date.date()) or not self.day_is_instructional(target_date):
            return None

        while cur_iter_day <= target_date:
            if self.day_is_instructional(cur_iter_day):
                if cycle_duration == 'day':
                    cycle_day_type_set.add(cur_iter_day.timetuple().tm_yday)
                elif cycle_duration == 'week':
                    cycle_day_type_set.add(cur_iter_day.isocalendar()[1])
                else:
                    raise NotImplementedError
            cur_iter_day += datetime.timedelta(1)

        return (len(cycle_day_type_set) - 1) % settings.TIMETABLE_FORMATS[self.timetable_format]['cycle']['length'] + 1

    def day_schedule_format(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()
        target_date = timezone.make_aware(datetime.datetime.combine(target_date, datetime.time(hour=11, minute=0, second=0)))

        schedule_formats = settings.TIMETABLE_FORMATS[self.timetable_format]['schedules']
        schedule_format_set = set(self.events.filter(start_date__lte=target_date, end_date__gte=target_date).values_list('schedule_format', flat=True)).intersection(set(schedule_formats.keys()))

        for schedule_format in list(schedule_formats.keys())[::-1]:
            if schedule_format in schedule_format_set: return schedule_format

        return 'default'

    def day_schedule(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()

        timetable_config = settings.TIMETABLE_FORMATS[self.timetable_format]
        day_num = self.day_num(target_date=target_date)

        if day_num is None:
            return []

        result = []

        for i in timetable_config['schedules'][self.day_schedule_format(target_date=target_date)]:
            start_time = timezone.make_aware(datetime.datetime.combine(target_date, datetime.time(*i['time'][0])))
            end_time = timezone.make_aware(datetime.datetime.combine(target_date, datetime.time(*i['time'][1])))

            result.append({
                'description': i['description'],
                'time': {
                    'start': start_time,
                    'end': end_time,
                },
                'courses': i['position'][day_num-1],
            })

        return result

class Course(models.Model):
    code = models.CharField(max_length=16)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'term'], name='unique_course'),
        ]

class Event(models.Model):
    name = models.CharField(max_length=128)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='events')
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="events", related_query_name="event")
    description = models.TextField(blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    schedule_format = models.CharField(max_length=64, default='default')
    is_instructional = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True, help_text='Whether if this event pertains to the general school population, not just those in the organization.')

    tags = models.ManyToManyField("Tag", blank=True, related_name="events", related_query_name="event")

    def __str__(self):
        return self.name

    def is_ongoing(self):
        today = timezone.localtime()
        return today >= self.start_date and today < self.end_date
