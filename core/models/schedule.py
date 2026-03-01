from django.db import models


class SchedulePattern(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    p1_start = models.TimeField()
    p1_end = models.TimeField()

    p2_start = models.TimeField()
    p2_end = models.TimeField()

    p3_start = models.TimeField()
    p3_end = models.TimeField()

    p4_start = models.TimeField()
    p4_end = models.TimeField()

    def __str__(self):
        return self.name


class ScheduleOverride(models.Model):
    date = models.DateField()
    pattern = models.ForeignKey(SchedulePattern, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.pattern.name}"
