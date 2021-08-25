from django.db import models
from django.urls import reverse
from metropolis import settings
from django.utils import timezone
import datetime

# Create your models here.

def is_instructional(day, events):
    return day.weekday() < 5 and not events.filter(is_instructional=False, start_date__lte=day, end_date__gt=day).exists()

class Term(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    timetable_format = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    is_frozen = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_ongoing(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()
        return target_date >= self.start_date and target_date < self.end_date

    def day(self, target_date=None):
        cycle_duration = settings.TIMETABLE_FORMATS[self.timetable_format]['cycle']['duration']
        events = Event.objects.filter(end_date__gt=self.start_date, start_date__lt=self.end_date , is_instructional=False)
        if target_date == None:
            target_date = timezone.localdate()
        cur_iter_day = self.start_date
        cycle_day_type_set = set()
        if not self.is_ongoing(target_date) or not is_instructional(target_date, events):
            return None
        while cur_iter_day <= target_date:
            if is_instructional(cur_iter_day, events):
                if cycle_duration == 'day':
                    cycle_day_type_set.add(cur_iter_day.timetuple().tm_yday)
                elif cycle_duration == 'week':
                    cycle_day_type_set.add(cur_iter_day.isocalendar()[1])
                else:
                    raise NotImplementedError
            cur_iter_day += datetime.timedelta(1)
        return (len(cycle_day_type_set) - 1) % settings.TIMETABLE_FORMATS[self.timetable_format]['cycle']['length'] + 1

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
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_instructional = models.BooleanField(default=False)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="events", related_query_name="event", blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="events", related_query_name="event")

    def __str__(self):
        return self.name

    def is_ongoing(self):
        today = timezone.localdate()
        if today >= self.start_date and today < self.end_date: return True
        else: return False
