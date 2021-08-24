from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
