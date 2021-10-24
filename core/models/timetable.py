from django.conf import settings
from django.db import models
from django.urls import reverse

from .. import utils
from .choices import timezone_choices
from .course import Course, Term

# Create your models here.


def get_default_timetable_format():
    return settings.DEFAULT_TIMETABLE_FORMAT


class Timetable(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="timetables"
    )
    term = models.ForeignKey(Term, on_delete=models.RESTRICT, related_name="timetables")
    courses = models.ManyToManyField(Course, related_name="timetables")

    def __str__(self):
        return (
            f"{self.owner.get_full_name()} ({self.owner})'s Timetable for {self.term}"
        )

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
                fields=["owner", "term"], name="unique_timetable_owner_and_term"
            )
        ]
