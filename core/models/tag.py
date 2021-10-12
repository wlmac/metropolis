import random

from django.db import models

from ..utils.tag_color import get_tag_color
from .organization import Organization

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(
        Organization, blank=True, null=True, default=None, on_delete=models.CASCADE
    )

    def color(self):
        random.seed(self.name + self.description)
        return get_tag_color(random.random())

    def __str__(self):
        return self.name
