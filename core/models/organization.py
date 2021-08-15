from django.db import models
from django.urls import reverse
from .user import User

# Create your models here.

class Organization(models.Model):
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="organizations_owning")
    supervisors = models.ManyToManyField("User", related_name="organizations_supervising")
    execs = models.ManyToManyField("User", related_name="organizations_leading")

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    registered_date = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="organizations", related_query_name="organization")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.pk])

    def member_count(self):
        return User.objects.filter(organizations=self).count()
