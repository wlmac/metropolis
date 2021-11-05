from django.conf import settings
from django.db import models
from django.urls import reverse

from ..utils.file_upload import file_upload_path_generator
from .post import Announcement
from .user import User

# Create your models here.


def banner_file_path_generator(instance, file_name):
    return file_upload_path_generator("banners")(instance, file_name)


def icon_file_path_generator(instance, file_name):
    return file_upload_path_generator("icons")(instance, file_name)


class Organization(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="organizations_owning",
    )
    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="organizations_supervising"
    )
    execs = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="organizations_leading"
    )

    name = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    extra_content = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    registered_date = models.DateTimeField(auto_now_add=True)
    show_members = models.BooleanField(default=True)
    is_open = models.BooleanField(default=True)
    applications_open = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="organizations", related_query_name="org"
    )

    banner = models.ImageField(
        upload_to=banner_file_path_generator, default="banners/default.png"
    )
    icon = models.ImageField(
        upload_to=icon_file_path_generator, default="icons/default.png"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.slug])

    def member_count(self):
        return User.objects.filter(organizations=self).count()

    def get_feed(self, user=None):
        org_feed = Announcement.get_approved().filter(organization=self)

        if user is None or user not in self.members.all():
            org_feed = org_feed.filter(is_public=True)

        return org_feed

    class Meta:
        verbose_name = "club"
        verbose_name_plural = "clubs"


class OrganizationURL(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="links"
    )
    url = models.URLField()

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Club URL"
        verbose_name_plural = "Club URLs"
