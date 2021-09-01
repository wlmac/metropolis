from django.db import models
from .choices import timezone_choices, graduating_year_choices
from django.contrib.auth.models import AbstractUser
from metropolis import settings

# Create your models here.

def get_default_user_timezone():
    return settings.DEFAULT_TIMEZONE

class User(AbstractUser):
    bio = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, choices=timezone_choices, default=get_default_user_timezone)
    graduating_year = models.PositiveSmallIntegerField(blank=True, null=True, choices=graduating_year_choices)
    organizations = models.ManyToManyField("Organization", blank=True, related_name="members", related_query_name="member")
    tags_following = models.ManyToManyField("Tag", blank=True, related_name="followers", related_query_name="follower")

    def get_ongoing_timetables(self):
        return [i for i in self.timetables.all() if i.term.is_ongoing()]
