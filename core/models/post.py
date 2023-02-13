from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
    show_after = models.DateTimeField(
        verbose_name="Automatically post on",
        help_text="Show this announcement after this time.",
    )

    title = models.CharField(max_length=64)
    body = models.TextField()
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="%(class)ss", related_query_name="%(class)s"
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ["-show_after"]


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

    def editable(self, user=None):
        if user is None:
            return False
        return user in (org := self.organization).supervisors.all() | org.execs.all()

    def approvable(self, user=None):
        if user is None:
            return False
        return user in (org := self.organization).supervisors.all()


def featured_image_file_path_generator(instance, file_name):
    return file_upload_path_generator("featured_image")(instance, file_name)


class BlogPost(Post):
    slug = models.SlugField(unique=True)
    featured_image = models.ImageField(
        upload_to=featured_image_file_path_generator,
        default="featured_image/default.png",
    )
    featured_image_description = models.CharField(
        help_text="Alt text for the featured image e.g. what screen readers tell users",
        max_length=140,
        default="",
        blank=True,
    )
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[self.slug])

    def increment_views(self) -> str:
        self.views += 1
        self.save()

    class Meta:
        ordering = ["-created_date"]
