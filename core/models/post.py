from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# from ..api.utils.profanity import predict
from ..utils.file_upload import file_upload_path_generator
from .choices import announcement_status_choices

# Create your models here.

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

    author: "User" | str = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET("[deleted]"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

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
        return self.author is None

    def get_object(
        self, obj: "PostInteraction", **kwargs
    ):  # get ken to check this in accordance with get
        content_type = ContentType.objects.get_for_model(obj)
        print(y := self.__class__.objects.get(), y.content_type, y.object_id)
        print(content_type, "a", obj.id, "b", kwargs)
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
        if kwargs.get("force", True):
            super().delete(using=using, keep_parents=keep_parents)
        self.user = None
        self.save()


class Comment(PostInteraction):
    """
    todo:
    - add a simple deletion system for staff and such

    """

    last_modified = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=512, null=True, blank=False)
    parent = models.ForeignKey(  # todo make sure parent isn't equal to self
        "Comment",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    likes = models.ManyToManyField(
        Like, blank=True, help_text="The users who liked this comment"
    )
    live = models.BooleanField(
        default=False,
        help_text="Shown publicly?",
    )  # todo run a simple profanity check on the comment and if it passes, it will be set to true

    def clean(self):
        if self.id == self.parent.id:
            raise ValidationError("A Comment cannot be a parent of itself.")
        return super().clean()

    def get_children(self):
        return Comment.objects.filter(parent=self, body__isnull=False)

    def delete(self, using=None, keep_parents=False, **kwargs):
        """
        Don't actually delete the object, just set the user to None and save it, that way you can still have sub comments.
        if force is set to True, then it will actually delete the object (used for when you want to delete a comment or unlike/save something)
        """
        if kwargs.get("force", True):
            if self.bottom_lvl:  # no sub comments
                super().delete(using=using, keep_parents=keep_parents)
            else:
                self.body = None
                self.author = None
                self.save()
        else:
            self.user = None
            self.save()

    @property
    def top_lvl(self) -> bool:
        """Returns True if the comment is a top level comment, False if it is a child comment."""
        return self.parent is None

    @property
    def bottom_lvl(self) -> bool:
        """Returns True if the comment is a bottom level comment, False if it is a parent comment."""
        return not self.get_children().exists()

    @property
    def like_count(self) -> int:
        return self.likes.objects.all().count()

    def flagged(self) -> bool:
        return self.__class__.objects.filter(live=False)

    def __str__(self) -> str:
        return str(self.body)

    def save(self, **kwargs):
        # todo run profanity check on body and if it passes, set live to True and save it. (see todo above)
        if not self.deleted and self.author.is_superuser:
            return super().save(**kwargs)
        # if bool(predict(self.body)[0]):  # 0.2ms per check, .5 for 10 and 3.5 for 100
        #    self.live = True todo reimpl profanity check
        self.live = True

        return super().save(**kwargs)

    @classmethod
    def scrub(cls):
        """
        Deletes all comments that have been deleted and now have no children.
        """
        comments = cls.objects.filter(body__isnull=True)
        map(lambda com: com.delete(), (x for x in comments if x.bottom_lvl))

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        permissions = (("view_flagged", "View flagged comments"),)


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

    likes = models.ManyToManyField(Like, blank=True)

    @property
    def comments(self):
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(
            content_type=content_type,
            object_id=self.id,
            parent=None,
        )

    @property
    def get_likes(self) -> int:
        return self.likes.objects.all().count()

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
                feed_all
                | approved_announcements.filter(organization__member=user)
                | cls.objects.filter(organization__execs__in=[user])
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
    last_modified_date = models.DateTimeField(auto_now_add=True)
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

    def increment_views(self) -> str:  # todo fix.
        self.views += 1
        self.save()

    class Meta:
        ordering = ["-created_date"]
