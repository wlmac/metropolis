from django.db import models
from .choices import timezone_choices, graduating_year_choices
from django.contrib.auth.models import AbstractUser
from metropolis import settings
from .course import Term
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

def get_default_user_timezone():
    return settings.DEFAULT_TIMEZONE

class User(AbstractUser):
    bio = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, choices=timezone_choices, default=get_default_user_timezone)
    graduating_year = models.PositiveSmallIntegerField(blank=True, null=True, choices=graduating_year_choices)
    organizations = models.ManyToManyField("Organization", blank=True, related_name="members", related_query_name="member")
    tags_following = models.ManyToManyField("Tag", blank=True, related_name="followers", related_query_name="follower")

    def get_ongoing_timetable(self):
        ongoing_term = Term.get_ongoing_term()
        if ongoing_term is None: return None

        try:
            return self.timetables.get(term=ongoing_term)
        except ObjectDoesNotExist:
            return None

    def schedule(self, target_date=None):
        if target_date == None:
            target_date = timezone.localdate()

        result = []

        for timetable in self.timetables.all():
            result.extend(timetable.day_schedule(target_date=target_date))

        result.sort(key=lambda x: (x['time']['start'], x['time']['end']))

        return result
