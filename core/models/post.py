from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ..utils.file_upload import file_upload_path_generator
from .choices import announcement_status_choices

# Create your models here.


class PostInteraction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(
            None
        ),  # todo check if user is deleted and if so set body to "deleted" and remove author from comment
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False, **kwargs):
        """
        Don't actually delete the object, just set the user to None and save it. This way, we can still keep track of the likes, saves and comments.
        if force is set to True, then it will actually delete the object (used for when you want to delete a comment or unlike/save something)
        """
        if kwargs.get("force", True):
            super().delete(using=using, keep_parents=keep_parents)
        self.user = None
        self.save()

    class Meta:
        abstract = True


class Like(PostInteraction):
    pass


class Save(PostInteraction):
    pass


class Comment(PostInteraction):
    """
    todo:
    - simplify the parental situation (X)
    - add a simple deletion system for staff and such
    - make sure body content is quickly checked for anything too bad (like profanity) and if so, set it to hidden and require approval from staff

    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )

    # above stuff is to allow for comments on comments and comments on both blog posts and announcements

    body = models.TextField(max_length=512)
    # todo check if owner is deleted and if so, just set comment body to "deleted" and remove author
    likes = models.ManyToManyField(Like, blank=True)
    saves = models.ManyToManyField(Save, blank=True)
    live = models.BooleanField(
        default=False
    )  # runs a simple profanity check on the comment and if it passes, it will be set to true

    def get_children(self):
        return Comment.objects.filter(parent_comment=self)

    def get_likes(self) -> int:
        return self.likes.objects.all().count()

    def __str__(self):
        return self.body

    def save(self, **kwargs):
        # todo run profanity check on body and if it passes, set live to True and save it.
        return super().save(**kwargs)

    class Meta:
        ordering = ["created_date"]


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
    saves = models.ManyToManyField(Save, blank=True)

    @property
    def comments(self):
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id, parent_comment=None)


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
