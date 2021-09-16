from django.db import models
import random
from .organization import Organization
from ..utils.tag_color import get_tag_color

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def color(self):
        random.seed(self.name + self.description)
        return get_tag_color(random.random())

    def __str__(self):
        return self.name
