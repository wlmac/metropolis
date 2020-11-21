from django.db import models
from django.urls import reverse
import datetime

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(max_length=128)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    num_courses = models.PositiveSmallIntegerField()
    timetable_format = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def is_ongoing(self):
        today = datetime.date.today()
        if today >= self.start_date and today < self.end_date: return True
        else: return False

class Course(models.Model):
    code = models.CharField(max_length=16)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('view_course', kwargs={'pk': self.pk})

    def __str__(self):
        return self.code
