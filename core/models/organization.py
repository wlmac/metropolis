import time

from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from .post import Announcement
from .user import User
from ..utils.file_upload import file_upload_path_generator


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
    is_active = models.BooleanField(default=True)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.owner_group = Group.objects.get(name="Org Owners")
        except Group.DoesNotExist:
            print(
                "Owners group does not exist, creating it but please add permissions to it"
            )
            self.owner_group = Group.objects.select_for_update().create(
                name="Org Owners"
            )

        try:
            self.execs_group = Group.objects.get(name="Execs")
        except Group.DoesNotExist:
            print(
                "Execs group does not exist, creating it but please add permissions to it"
            )
            self.execs_group = Group.objects.select_for_update().create(name="Execs")

    def __str__(self):
        return self.name

    @classmethod
    def active(cls):
        return cls.objects.filter(is_active=True)

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


@receiver(post_save, sender=Organization)
def manage_org_groups(sender, instance, created, raw, update_fields, **kwargs):
    obj = Organization.objects.get(id=instance.id)  #
    print("obj execs", obj.execs.all())

    from ..tasks import clear_unused_users  # remove this when the below works

    print("execs", instance.execs.all())
    print("owner", instance.owner)

    owner_group, _ = Group.objects.get_or_create(name="Org Owners")
    execs_group, _ = Group.objects.get_or_create(name="Execs")
    if created:  # if the org is being created
        instance.owner.groups.add(owner_group)
        for user in instance.execs.all():
            user.groups.add(instance.execs_group)

    else:
        # if "execs" in update_fields: wait until django 4.2 for this and the one below as it will not work yet.
        handle_execs(execs_group, instance)
        # if "owner" in update_fields:
        handle_owner(owner_group, instance)

        clear_unused_users()  # todo remove this when the above works


def handle_owner(group: Group, instance: Organization):
    instance.owner.groups.add(group)
    print(f"Added {instance.owner} to owners group")


def handle_execs(group: Group, instance: Organization):
    execs = Organization.objects.get(id=instance.id).execs.all()
    print("execs in handle", execs)
    for user in instance.execs.all():
        user.groups.add(group)
        print(f"Added {user} to execs group")
