from django.conf import settings
from django.db import models

from .course import Course
from ..utils import get_day_schedule

# Create your models here.


def get_default_timetable_format():
    return settings.DEFAULT_TIMETABLE_FORMAT


def default_courses():
    return ["" for i in range(4)]


class SchedulePattern(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    p1_start = models.TimeField()
    p1_end = models.TimeField()

    p2_start = models.TimeField()
    p2_end = models.TimeField()

    p3_start = models.TimeField()
    p3_end = models.TimeField()

    p4_start = models.TimeField()
    p4_end = models.TimeField()

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "p1_start": self.p1_start,
            "p1_end": self.p1_end,
            "p2_start": self.p2_start,
            "p2_end": self.p2_end,
            "p3_start": self.p3_start,
            "p3_end": self.p3_end,
            "p4_start": self.p4_start,
            "p4_end": self.p4_end,
        }


class ScheduleOverride(models.Model):
    date = models.DateField()
    pattern = models.ForeignKey(SchedulePattern, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.pattern.name}"


class Timetable(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timetable",
    )
    courses = models.ManyToManyField(Course, related_name="timetables")
    title = models.CharField(max_length=64, blank=False, default="New timetable")
    courses_str = models.JSONField(blank=True, default=default_courses)

    def __str__(self):
        return f"{self.owner.get_full_name()} ({self.owner})'s Timetable '{self.title}'"

    def clean(self, *args, **kwargs):
        if len(self.courses_str) != 4:
            raise ValueError("Timetable must have 4 periods")
        self.courses_str = [course.strip() for course in self.courses_str]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def day_schedule(self, target_date=None):
        return get_day_schedule(date=target_date, user=self.owner)
