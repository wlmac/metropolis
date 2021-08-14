from django.db import models
from django.urls import reverse
from metropolis import settings
from django.utils import timezone
import datetime

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_ongoing_terms(self):
        return [term for term in self.terms.all() if term.is_ongoing()]

def is_instructional(day, events):
    return day.weekday() < 5 and not events.filter(is_instructional=False, start_date__lte=day, end_date__gt=day).exists()

class Term(models.Model):
    name = models.CharField(max_length=128)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='terms')
    description = models.TextField(blank=True)
    num_courses = models.PositiveSmallIntegerField()
    timetable_format = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    is_frozen = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_ongoing(self):
        today = timezone.localdate()
        if today >= self.start_date and today < self.end_date: return True
        else: return False

    def day(self):
        events = Event.objects.filter(term=self, is_instructional=False)
        today = timezone.localdate()
        cur_iter_day = self.start_date
        day_num = 0
        if not is_instructional(today, events):
            return None
        while cur_iter_day < today:
            if is_instructional(cur_iter_day, events):
                day_num += 1
            cur_iter_day += datetime.timedelta(1)
        return day_num % settings.TIMETABLE_FORMATS[self.timetable_format]['days'] + 1

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
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_instructional = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_ongoing(self):
        today = timezone.localdate()
        if today >= self.start_date and today < self.end_date: return True
        else: return False
