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

    def get_absolute_url(self):
        return reverse('view_timetable', kwargs={'pk': self.pk})

    class Meta:
        constraints = [models.UniqueConstraint(fields=['owner', 'term'], name='unique_timetable_owner_and_term')]
