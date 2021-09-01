from django.db import models
from .choices import announcement_status_choices

# Create your models here.

class Announcement(models.Model):
    author = models.ForeignKey("User", null=True, on_delete=models.SET_NULL, related_name="announcements_authored")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128, blank=True)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="announcements", related_query_name="announcement")

    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="announcements", related_query_name="announcement")

    is_public = models.BooleanField(default=True, help_text='Whether if this announcement pertains to the general school population, not just those in the organization.')
    supervisor = models.ForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL, related_name="announcements_approved")
    status = models.CharField(max_length=1, choices=announcement_status_choices, default='p')
    rejection_reason = models.CharField(max_length=140, blank=True, verbose_name='reason for rejection', help_text='Only fill this field in if you are rejecting this announcement.')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("announcement_detail", args=[self.slug])

    class Meta:
        ordering = ['-last_modified_date']
