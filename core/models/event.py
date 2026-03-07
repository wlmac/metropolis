from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(max_length=150, blank=False)

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="events",
        related_query_name="event",
    )
    description = models.TextField(blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()  # todo fix this

    schedule_format = models.CharField(max_length=64, default="default")
    is_instructional = models.BooleanField(
        help_text="Whether or not school is running on this day. Automatically changes depending on the schedule format and should not be manually edited.",
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether or not this event is viewable to the general school population, not just those in the organization.",
    )
    should_announce = models.BooleanField(
        default=False,
        help_text="Whether or not this event should be announced to the general school population VIA the important events feed.",
    )

    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="events", related_query_name="event"
    )

    gcal_id = models.CharField(
        max_length=1024,
        default=None,
        null=True,
        unique=True,
        editable=False,
        help_text="Unique identifier for events that are automatically created using data from the official WLMAC calendar. Should not be manually edited.",
    )

    def __str__(self):
        return self.name

    def is_current(self):
        today = timezone.localtime()
        return self.start_date <= today < self.end_date

    @classmethod
    def get_events(cls, user=None):
        events = cls.objects.filter(is_public=True)
        if user is not None and user.is_authenticated:
            events = (events | events.filter(organization__member=user)).distinct()

        return events

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                {
                    "start_date": _("Start date must be before end date"),
                    "end_date": _("Start date must be before end date"),
                }
            )

    def save(self, *args, **kwargs):
        if not timezone.is_aware(self.end_date):
            # Convert naive datetime to aware datetime
            self.end_date = timezone.make_aware(
                self.end_date, timezone.get_current_timezone()
            )
        if not timezone.is_aware(self.start_date):
            # Convert naive datetime to aware datetime
            self.start_date = timezone.make_aware(
                self.start_date, timezone.get_current_timezone()
            )

        self.clean()
        super().save(*args, **kwargs)
