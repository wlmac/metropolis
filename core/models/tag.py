import random

from django.db import models

from .organization import Organization
from ..utils.tag_color import get_tag_color


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(
        Organization, blank=True, null=True, default=None, on_delete=models.CASCADE
    )

    @property
    def color(self) -> str:
        """
        Returns a random color based on the tag's name and description.
        
        :return: A color in hex format.
        """
        random.seed(self.name + self.description)
        return get_tag_color(random.random())

    def __str__(self):
        return self.name

    def editable(self, user=None):
        if user is None:
            return False
        return user in (org := self.organization).supervisors.all() | org.execs.all()
