from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .choices import REQUEST_STATUS_CHOICES

class PubReq(models.Model):
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'object_id')

    request_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="pubreqs",
    )
    requesters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='supporting_pubreqs',
    )
    approvers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='pubreqs_to_approve',
    )
    status = models.CharField(
        max_length=1,
        choices=REQUEST_STATUS_CHOICES,
    )
    rej_why = models.CharField(
        max_length=140,
        blank=True,
        verbose_name="reason for rejection",
        help_text="Only fill this field in if you are rejecting this request.",
    )

    @classmethod
    def get_all(cls, user=None):
        if user is None:
            return cls.objects.none()
        else:
            return cls.objects.filter(
                models.Q(requesters__in=[user]) |
                models.Q(approvers__in=[user])
            )

    def get_absolute_url(self):
        return reverse("appreq_detail", args=[self.pk])

    def __str__(self):
        return f"RfP for {self.target}"

    @property
    def title(self):
        return f"Request for Publishing for {self.target}"

    class Meta:
        verbose_name = "Request for Pubblishing"
        verbose_name_plural = "Requests for Pubblishing"
