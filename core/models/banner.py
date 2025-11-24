from django.db import models
from django.core.exceptions import ValidationError


class Banner(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Give the banner a name! Only used for admin purposes to differentiate banners, not displayed elsewhere",
    )

    content = models.CharField(max_length=200)
    icon_url = models.CharField(max_length=150, blank=True)

    cta_link = models.CharField(max_length=150, blank=True)
    cta_label = models.CharField(
        max_length=100, help_text="Required only if cta_link is present", blank=True
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        errors = {}

        if self.cta_link and not self.cta_label:
            errors["cta_label"] = "cta label must be present if cta link is present"

        if self.end_date and self.start_date and self.end_date < self.start_date:
            errors["end_date"] = "End date must be after start date"

        if errors:
            raise ValidationError(errors)

        return super().clean()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="cta_label_requirement",
                check=models.Q(cta_link="")
                | (~models.Q(cta_link="") & ~models.Q(cta_label="")),
            ),
            models.CheckConstraint(
                name="end_date_gte_to_start_date",
                check=models.Q(end_date__gte=models.F("start_date")),
            ),
        ]
