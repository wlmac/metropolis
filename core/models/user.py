from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .choices import graduating_year_choices, timezone_choices
from .course import Term
from .post import Announcement
from ..utils.fields import SetField


# Create your models here.


def get_default_user_timezone():
    return settings.DEFAULT_TIMEZONE


class User(AbstractUser):
    bio = models.TextField(blank=True)
    timezone = models.CharField(
        max_length=50, choices=timezone_choices, default=get_default_user_timezone
    )
    graduating_year = models.PositiveSmallIntegerField(
        blank=True, null=True, choices=graduating_year_choices
    )
    is_teacher = models.BooleanField(default=False)
    organizations = models.ManyToManyField(
        "Organization", blank=True, related_name="members", related_query_name="member"
    )
    tags_following = models.ManyToManyField(
        "Tag", blank=True, related_name="followers", related_query_name="follower"
    )
    qltrs = SetField("Qualified Trials", null=True, blank=True)
    saved_blogs = models.ManyToManyField("BlogPost", blank=True)
    saved_announcements = models.ManyToManyField("Announcement", blank=True)

    expo_notif_token = models.TextField(
        "Expo Notifications Token",
        blank=True,
        null=True,
        # the length is not specified :( https://github.com/expo/expo/issues/1135#issuecomment-399622890
    )

    @property
    def qltrs2(self):
        return set(self.qltrs.split(" "))

    def in_qltr(self, name: str):
        if self.qltrs:
            return name in self.qltrs
        return False

    def get_current_timetable(self):
        current_term = Term.get_current()
        if current_term is None:
            return None

        try:
            return self.timetables.get(term=current_term)
        except ObjectDoesNotExist:
            return None

    def schedule(self, target_date=None):
        if target_date is None:
            target_date = timezone.localdate()

        result = []

        for timetable in self.timetables.all():
            result.extend(timetable.day_schedule(target_date=target_date))

        result.sort(key=lambda x: (x["time"]["start"], x["time"]["end"]))

        return result

    def get_feed(self):
        return (
            Announcement.get_approved()
            .filter(
                Q(is_public=True, tags__follower=self) | Q(organization__member=self)
            )
            .distinct()
        )

    @property
    def staff_bio(self):
        if self.pk in settings.METROPOLIS_STAFF_BIO:
            return settings.METROPOLIS_STAFF_BIO[self.pk]
        else:
            return None

    def can_edit(self, obj):
        return obj.editable(user=self)

    def can_approve(self, obj):
        return obj.approvable(user=self)

    @classmethod
    def all(cls):
        return cls.objects.filter(is_active=True)
