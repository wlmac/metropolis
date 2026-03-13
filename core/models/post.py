from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone

# from ..api.utils.profanity import predict
from ..utils.file_upload import file_upload_path_generator
from .choices import announcement_status_choices

if TYPE_CHECKING:
    from .user import User


class PostInteraction(models.Model):
    """
    how to fetch a PostInteraction object:


    content_type = ContentType.objects.get_for_model(self)
        return PostInteraction.objects.filter(
            content_type=content_type, object_id=self.id
        )

    """

    author: User | str = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET(None),
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # --- Generic Foreign Key --- #
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="The type of object this comment is on (core | blog post or core | announcement)",
    )
    object_id = models.PositiveIntegerField(
        help_text="The id of the object this comment is on"
    )
    content_object = GenericForeignKey("content_type", "object_id")

    # --- Generic Foreign Key --- #

    @property
    def deleted(self):
        return self.created_at is None

    def get_object(
        self, obj: PostInteraction, **kwargs
    ):  # get ken to check this in accordance with get
        content_type = ContentType.objects.get_for_model(obj)
        return self.__class__.objects.filter(
            content_type=content_type, object_id=obj.id, **kwargs
        )

    class Meta:
        abstract = True


class Like(PostInteraction):
    def delete(self, using=None, keep_parents=False, **kwargs):
        """
        Don't actually delete the object, just set the user to None and save it. This way, we can still keep track of the likes, saves and comments.
        if force is set to True, then it will actually delete the object (used for when you want to delete a comment or unlike/save something)
        """
        if kwargs.get("force", False):
            return super().delete(using=using, keep_parents=keep_parents)
        self.user = None
        self.save()


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
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
        "Tag",
        blank=True,
        related_name="%(class)ss",
        related_query_name="%(class)s",
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
        blank=True,
        null=True,
    )

    organization_string = models.CharField(max_length=64, blank=True, null=True)

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
    def get_approved(cls) -> QuerySet:
        return (
            cls.objects.filter(status="a")
            .filter(show_after__lte=timezone.now())
            .order_by("-show_after", "-pk")
        )

    @classmethod
    def get_all(cls, user=None) -> QuerySet:
        approved_announcements = cls.get_approved()

        if user is not None and user.is_superuser:
            return approved_announcements  # return all announcements if user is superuser (admin).

        feed_all = approved_announcements.filter(is_public=True)
        if user is not None and user.is_authenticated:
            feed_all = (
                feed_all
                | approved_announcements.filter(organization__member=user)
                | cls.objects.filter(organization__execs__in=[user])
            ).distinct()
        feed = feed_all
        return feed

    def editable(self, user=None):
        if user.is_superuser:
            return True
        if user is None:
            return False
        return user in (org := self.organization).supervisors.all() | org.execs.all()

    def approvable(self, user=None):
        if user is None:
            return False
        return self.organization.supervisors.filter(user=user).exists()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="organization_or_organization_string_required",
                condition=models.Q(organization__isnull=False)
                | models.Q(organization_string__isnull=False),
            )
        ]


def featured_image_file_path_generator(instance, file_name):
    return file_upload_path_generator("featured_image")(instance, file_name)


class BlogPost(Post):
    slug = models.SlugField(unique=True)
    featured_image = models.ImageField(
        upload_to=featured_image_file_path_generator,
        default="featured_image/default.png",
    )
    last_modified_date = models.DateTimeField(auto_now_add=True)
    featured_image_description = models.CharField(
        help_text="Alt text for the featured image e.g. what screen readers tell users",
        max_length=140,
        default="",
        blank=True,
    )
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    is_archived = models.BooleanField(
        default=False,
        help_text="Archived posts are not shown on the blog page.",
    )

    @classmethod
    def public(cls):
        return cls.objects.filter(
            is_published=True, is_archived=False, show_after__lte=timezone.now()
        )

    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[self.slug])

    def increment_views(self) -> str:
        self.views += 1
        self.save()

    class Meta:
        ordering = ["-created_date"]
        indexes = [
            models.Index(fields=["is_archived"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["created_date"], name="idx_created_date"),
        ]


class Exhibit(Post):
    slug = models.SlugField(unique=True)
    content = models.ImageField(
        upload_to=featured_image_file_path_generator,
        default="featured_image/default.png",
    )
    content_description = models.CharField(
        help_text="Alt text for the featured image e.g. what screen readers tell users",
        max_length=140,
    )
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_date"]
