from django.db import models
import random
import colorsys
from metropolis import settings

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def color(self):
        random.seed(self.name + self.description)
        hue = random.random()
        return '#%02x%02x%02x' % tuple(int(i*255) for i in colorsys.hsv_to_rgb(hue, settings.TAG_COLOR_SATURATION, settings.TAG_COLOR_VALUE))

    def __str__(self):
        return self.name
