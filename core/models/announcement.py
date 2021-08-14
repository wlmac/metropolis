from django.db import models

# Create your models here.

class Announcement(models.Model):
    authors = models.ManyToManyField("User")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128, blank=True)
    body = models.TextField(blank=True)
    summary = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)

    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="announcements", related_query_name="announcement")
    approver = models.ForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL, related_name="announcements_approved")
    is_public = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True, related_name="announcements", related_query_name="announcement")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("announcement_detail", args=[self.slug])
