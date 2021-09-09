from django.db import models
from django.urls import reverse
from .user import User
from ..utils.file_upload import file_upload_path_generator

# Create your models here.

def banner_file_path_generator(instance, file_name):
    return file_upload_path_generator('banners')(instance, file_name)

def icon_file_path_generator(instance, file_name):
    return file_upload_path_generator('icons')(instance, file_name)

class Organization(models.Model):
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="organizations_owning")
    supervisors = models.ManyToManyField("User", related_name="organizations_supervising")
    execs = models.ManyToManyField("User", related_name="organizations_leading")

    name = models.CharField(max_length=64)
    bio = models.CharField(blank=True, max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    registered_date = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    applications_open = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True, related_name="organizations", related_query_name="organization")

    banner = models.ImageField(blank=True, upload_to=banner_file_path_generator, default='banners/default.png')
    icon = models.ImageField(blank=True, upload_to=icon_file_path_generator, default='icons/default.png')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.slug])

    def member_count(self):
        return User.objects.filter(organizations=self).count()

    class Meta:
        verbose_name = 'club'

class OrganizationURL(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()

    def __str__(self):
        return self.url
