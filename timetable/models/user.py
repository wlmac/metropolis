from django.db import models
from .choices import timezone_choices
from .course import School
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    description = models.TextField(blank=True)
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, choices=timezone_choices, default="UTC")
