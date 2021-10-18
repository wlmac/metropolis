from django.conf import settings
from django.db import models
from django.urls import reverse

from ..utils.file_upload import file_upload_path_generator
from .choices import announcement_status_choices

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)ss_authored",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=64, blank=True)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="%(class)ss", related_query_name="%(class)s"
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ["-created_date"]


class Announcement(Post):
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="announcements",
        related_query_name="announcement",
    )

    is_public = models.BooleanField(
        default=True,
        help_text="Whether if this announcement pertains to the general school population, not just those in the organization.",
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="announcements_approved",
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

    def get_absolute_url(self):
        return reverse("announcement_detail", args=[self.pk])

    @classmethod
    def get_approved(cls):
        return cls.objects.filter(status="a")

    @classmethod
    def get_all(cls, user=None):
        approved_announcements = cls.get_approved()

        feed_all = approved_announcements.filter(is_public=True)
        if user is not None and user.is_authenticated:
            feed_all = (
                feed_all | approved_announcements.filter(organization__member=user)
            ).distinct()

        return feed_all


def featured_image_file_path_generator(instance, file_name):
    return file_upload_path_generator("featured_image")(instance, file_name)


class BlogPost(Post):
    slug = models.SlugField(unique=True)
    featured_image = models.ImageField(
        upload_to=featured_image_file_path_generator,
        default="featured_image/default.png",
    )
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[self.slug])

    class Meta:
        ordering = ["-created_date"]
