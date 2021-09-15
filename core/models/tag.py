from django.db import models
import random
from ..utils.tag_color import get_tag_color

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def color(self):
        random.seed(self.name + self.description)
        return get_tag_color(random.random())

    def __str__(self):
        return self.name
