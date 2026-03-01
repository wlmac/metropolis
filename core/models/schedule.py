from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.db.models import F, Q, functions


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

    def clean(self):
        super().clean()

        errors = {}

        if (
            SchedulePattern.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = "Schedule pattern with this name already exists"

        fields = [
            "p1_start",
            "p1_end",
            "p2_start",
            "p2_end",
            "p3_start",
            "p3_end",
            "p4_start",
            "p4_end",
        ]

        for i in range(len(fields) - 1):
            f1, f2 = fields[i], fields[i + 1]
            if not getattr(self, f1) <= getattr(self, f2):
                p = lambda f: f"P{f[1]} {f[3:]}"  # noqa: E731

                errors[f2] = f"{p(f2)} cannot be before {p(f1)}"
                errors[NON_FIELD_ERRORS] = (
                    "All period start/end times must be in increasing order"
                )

        if errors:
            raise ValidationError(
                errors,
                code="invalid",
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                functions.Lower("name"),
                name="unique_pattern_name",
            ),
            models.CheckConstraint(
                name="period_times_in_order",
                condition=(
                    Q(p1_start__lte=F("p1_end"))
                    & Q(p1_end__lte=F("p2_start"))
                    & Q(p2_start__lte=F("p2_end"))
                    & Q(p2_end__lte=F("p3_start"))
                    & Q(p3_start__lte=F("p3_end"))
                    & Q(p3_end__lte=F("p4_start"))
                    & Q(p4_start__lte=F("p4_end"))
                ),
            ),
        ]


class ScheduleOverride(models.Model):
    date = models.DateField(unique=True)
    pattern = models.ForeignKey(SchedulePattern, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.pattern.name}"
