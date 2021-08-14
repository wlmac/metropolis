from django.db import models
from .choices import timezone_choices
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    description = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, choices=timezone_choices, default="UTC")

    def get_ongoing_timetables(self):
        return [i for i in self.timetables.all() if i.term.is_ongoing()]
