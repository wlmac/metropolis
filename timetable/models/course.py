from django.db import models

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

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=16)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.code
