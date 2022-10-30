from django.db import models

from .util import SetField


class Raffle(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    open_start = models.DateTimeField()
    open_end = models.DateTimeField()
    page_win = models.CharField(max_length=128)
    page_lose = models.CharField(max_length=128)
    codes_win = SetField("Winning Codes", null=True, blank=True)

    def __str__(self):
        return self.name
