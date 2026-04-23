from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
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
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="organizations_owning",
    )
    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="organizations_supervising",
    )
    execs = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="organizations_leading"
    )

    name = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    extra_content = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    registered_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="organizations",
        related_query_name="org",
    )

    banner = models.ImageField(
        upload_to=banner_file_path_generator, default="banners/default.png"
    )
    icon = models.ImageField(
        upload_to=icon_file_path_generator, default="icons/default.png"
    )

    def __str__(self):
        return self.name

    @classmethod
    def active(cls):
        return cls.objects.filter(is_active=True)

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.slug])

    def follower_count(self):
        return User.objects.filter(organizations=self).count()

    def get_feed(self, user=None):
        org_feed = Announcement.get_approved().filter(organization=self)

        if user is None or user not in self.followers.all():
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


@receiver(m2m_changed, sender=Organization.owners.through)
@receiver(m2m_changed, sender=Organization.execs.through)
@receiver(m2m_changed, sender=Organization.supervisors.through)
def manage_org_roles(sender, instance, action, reverse, model, pk_set, **kwargs):
    owner_group, _ = Group.objects.get_or_create(name="Org Owners")
    execs_group, _ = Group.objects.get_or_create(name="Execs")
    supervisors_group, _ = Group.objects.get_or_create(name="Supervisors")

    match sender:
        case Organization.owners.through:
            groups = [owner_group, execs_group]
        case Organization.execs.through:
            groups = [execs_group]
        case Organization.supervisors.through:
            groups = [supervisors_group]
        case _:
            return

    users = User.objects.filter(pk__in=pk_set)

    if action == "post_add":
        for user in users:
            for group in groups:
                user.groups.add(group)
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=["is_staff"])

    elif action == "post_remove":
        for user in users:
            is_still_org_owner = user.organizations_owning.exists()
            is_still_org_exec = user.organizations_leading.exists()
            is_still_org_supervisor = user.organizations_supervising.exists()

            if owner_group in groups and not is_still_org_owner:
                user.groups.remove(owner_group)
            if execs_group in groups and not is_still_org_exec:
                user.groups.remove(execs_group)
            if supervisors_group in groups and not is_still_org_supervisor:
                user.groups.remove(supervisors_group)

            if all(
                [
                    user.is_staff,
                    not user.is_superuser,
                    not user.is_teacher,
                    not is_still_org_owner,
                    not is_still_org_exec,
                    not is_still_org_supervisor,
                ]
            ):
                user.is_staff = False
                user.save(update_fields=["is_staff"])
