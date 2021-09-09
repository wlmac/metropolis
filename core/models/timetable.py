from django.db import models
from .choices import timezone_choices
from django.contrib.auth import get_user_model
from .user import User
from .course import Term, Course
from metropolis import settings
from django.urls import reverse

# Create your models here.

def get_default_timetable_format():
    return settings.DEFAULT_TIMETABLE_FORMAT

class Timetable(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='timetables')
    term = models.ForeignKey(Term, on_delete=models.RESTRICT, related_name='timetables')
    courses = models.ManyToManyField(Course, related_name='timetables')

    def __str__(self):
        return f'{self.owner.get_full_name()} ({self.owner})\'s Timetable for {self.term}'

    def day_schedule(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()

        courses = {}
        for i in self.courses.all():
            courses[i.position] = i

        result = self.term.day_schedule(target_date=target_date)

        for i in range(0, len(result)):
            course_positions = result[i].pop('courses')

            try:
                course_code = courses[course_positions.intersection(set(courses.keys())).pop()].code
            except KeyError:
                course_code = None

            result[i]['course'] = course_code

        return result

    class Meta:
        constraints = [models.UniqueConstraint(fields=['owner', 'term'], name='unique_timetable_owner_and_term')]
