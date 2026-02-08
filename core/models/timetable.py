from django.conf import settings
from django.db import models

from .. import utils
from .course import Course, Term

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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timetables",
    )
    term = models.ForeignKey(Term, on_delete=models.RESTRICT, related_name="timetables")
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
        # TODO: Drop timetable if owner makes too many?
        super().save(*args, **kwargs)

    def day_schedule(self, target_date=None):
        target_date = utils.get_localdate(date=target_date)

        courses = {}
        for i in self.courses.all():
            courses[i.position] = i

        result = self.term.day_schedule(target_date=target_date)

        for i in range(0, len(result)):
            course_positions = result[i]["position"]

            try:
                course_code = courses[
                    course_positions.intersection(set(courses.keys())).pop()
                ].code
            except KeyError:
                course_code = None

            result[i]["course"] = course_code

        merged_result = []

        cur_period_idx = 0
        while cur_period_idx < len(result):
            merged_result.append(result[cur_period_idx])
            cur_course = result[cur_period_idx]["course"]
            while (
                cur_period_idx + 1 < len(result)
                and cur_course is not None
                and cur_course == result[cur_period_idx + 1]["course"]
            ):
                cur_period_idx += 1
                merged_result[-1]["time"]["end"] = result[cur_period_idx]["time"]["end"]
            cur_period_idx += 1

        return merged_result

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "term"],
                name="unique_timetable_owner_and_term",
            )
        ]
