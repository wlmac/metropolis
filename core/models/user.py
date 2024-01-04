from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q, CharField
from django.db.models.functions import Lower
from django.utils import timezone

from .choices import graduating_year_choices, timezone_choices
from .course import Term
from .post import Announcement
from ..utils import calculate_years
from ..utils.fields import SetField, ArrayField


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

    expo_notif_tokens = models.JSONField(
        "Expo Notifications Tokens",
        default=dict,
        help_text="JSON object with keys as tokens and values as null.",
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

    def can_edit(self, obj):
        return obj.editable(user=self)

    def can_approve(self, obj):
        return obj.approvable(user=self)

    @classmethod
    def all(cls):
        return cls.objects.filter(is_active=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("username"), name="username-lower-check")
        ]


class StaffMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="staff")
    bio = models.TextField(blank=False, null=False, help_text="The users staff bio (displayed on the staff page).")
    _positions_options = tuple(settings.METROPOLIS_POSITIONS.items())
    positions = ArrayField(base_field=CharField(choices=_positions_options), help_text="The positions the user had/does hold.")
    positions_leading = ArrayField(
        blank=True,
        null=True,
        base_field=CharField(choices=tuple(({key: val for key,
        val in _positions_options if key != 'PM'}).items())), # remove PM from the list of positions leading as all PM's are leading PM
    )

    years = ArrayField(base_field=CharField(choices=calculate_years(fmt="generate")), help_text="The years the user was a staff member. Used to determine if the user is an alumni.")
    is_active = models.BooleanField(default=True, help_text="If the user is no longer a member of metro for whatever reason. Toggle this instead of deleting.") # if the user got kicked or smth

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user})"

    @property
    def is_alumni(self):
        return calculate_years("is_alumni", self.years)

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="unique_staff_member",
            )
        ]
