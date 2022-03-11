from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from ..utils.file_upload import file_upload_path_generator
from .choices import announcement_status_choices


class RfP(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="rfps_authored",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="rfps_supervised",
    )
    status = models.CharField(
        max_length=1, choices=announcement_status_choices, default="p"
    )
    rejection_reason = models.CharField(
        max_length=140,
        blank=True,
        verbose_name="reason for rejection",
        help_text="Only fill this field in if you are rejecting this announcement.",
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "RfP for {}".format(self.content_object)

    @classmethod
    def accessible_by(cls, user):
        if user.is_superuser:
            return cls.objects.all()
        return cls.objects.filter(
            models.Q(is_public=True, status="a")
            | models.Q(author=user)
            | models.Q(supervisor=user)
        )

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "RfP"
