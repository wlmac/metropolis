from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q, CharField
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from . import timezone_choices, graduating_year_choices
from .course import Term
from .post import Announcement
from ..utils.choices import calculate_years
from ..utils.fields import SetField, ChoiceArrayField
from ..utils.mail import send_mail


# Create your models here.


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        By default, Django does a case-sensitive check on usernames. This is Wrong™.
        Overriding this method fixes it.
        """
        return self.get(**{self.model.USERNAME_FIELD + "__iexact": username})


def get_default_user_timezone():
    return settings.DEFAULT_TIMEZONE


class User(AbstractUser):
    objects = CaseInsensitiveUserManager()
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
    is_deleted = models.BooleanField(default=False, help_text="If the user is deleted. Never change this in admin", null=False, blank=False)
    deleted_at = models.DateTimeField(null=True, default=None, blank=True, help_text="When the user was deleted. Never change this in admin")

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

    def mark_deleted(self):
        self.is_deleted = True
        self.last_login = timezone.now()
        self.save()
        email_template_context = {
            "user": self,
            "time_deleted": timezone.now(),
            "restore_link": settings.SITE_URL + reverse("restore", args=(self.id,)),
        }

        send_mail(  # todo: frontend needs to make a page for this
            f"[ACTION REQUIRED] Your account has been marked for deletion.",
            render_to_string(
                "core/email/restore_deleted_user.txt",
                email_template_context,
            ),
            None,
            [self.email],
            html_message=render_to_string(
                "core/email/restore_deleted_user.html",
                email_template_context,
            ),
        )
        
    def mark_restored(self):
        self.is_deleted = True
        self.last_login = timezone.now()
        self.save()
        email_template_context = {
            "user": self,
        }
        
        send_mail(  # todo: frontend needs to make a page for this
            f"Your account has successfully been restored.",
            render_to_string(
                "core/email/restored_user.txt",
                email_template_context,
            ),
            None,
            [self.email],
            html_message=render_to_string(
                "core/email/restored_user.html",
                email_template_context,
            ),
        )
    @classmethod
    def all(cls):
        return cls.objects.filter(is_active=True)


class StaffMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="staff",
    )
    bio = models.TextField(
        blank=False,
        null=False,
        help_text="The users staff bio (displayed on the staff page).",
    )
    positions = ChoiceArrayField(
        base_field=CharField(choices=settings.METROPOLIS_POSITIONS),
        help_text="The positions the user had/does hold.",
    )
    positions_leading = ChoiceArrayField(
        blank=True,
        null=True,
        base_field=CharField(
            choices=[
                (key, val)
                for key, val in settings.METROPOLIS_POSITIONS
                if key != "Project Manager"
            ]
        ),
    )

    years = ChoiceArrayField(
        base_field=CharField(choices=calculate_years(fmt="generate")),
        help_text="The years the user was a staff member. Used to determine if the user is an alumni.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="If the user is no longer a member of metro for whatever reason. Toggle this instead of deleting.",
    )  # if the user got kicked or smth

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user})"

    @property
    def is_alumni(self):
        return calculate_years("is_alumni", self.years)

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
