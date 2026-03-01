from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ..utils import get_day_schedule


class Course(models.Model):
    timetable = models.ForeignKey(
        "Timetable",
        on_delete=models.CASCADE,
        related_name="courses",
    )
    period = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    name = models.CharField(max_length=32, blank=True)
    room = models.CharField(max_length=16, blank=True)
    teacher = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"Period {self.period}: '{self.name}' for {self.timetable}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["timetable", "period"],
                name="unique_period_per_timetable_course",
            )
        ]
        ordering = ["period"]


class Timetable(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timetable",
    )
    title = models.CharField(max_length=64, blank=False, default="My timetable")

    def day_schedule(self, target_date=None):
        return get_day_schedule(date=target_date, user=self.owner)

    def get_courses_as_dict(self):
        return {
            course.period: {
                "name": course.name,
                "room": course.room,
                "teacher": course.teacher,
            }
            for course in self.courses.all()
        }

    def clear_courses(self):
        for course in self.courses.all():
            course.delete()
        return self

    def __str__(self):
        return f"{self.owner.get_full_name()} ({self.owner})'s Timetable '{self.title}'"
