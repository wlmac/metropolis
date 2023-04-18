from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import PositiveIntegerRelDbTypeMixin, SmallIntegerField
from django.forms import DateInput, DateField
from django.utils.dateparse import parse_date
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _


class MonthDayFormField(DateField):
    """
    A custom form field that only allows month/day dates to be entered.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widget = MonthDayInput()

    def to_python(self, value):
        """
        Parses a string value representing a month/day date into a datetime.date
        object with the current year.
        """
        if not value:
            return None
        try:
            month, day = value.split("/")
            return (
                datetime.now()
                .replace(year=datetime.now().year, month=int(month), day=int(day))
                .date()
            )
        except ValueError:
            raise ValidationError(_("Invalid date format (must be MM/DD)"))

    def prepare_value(self, value) -> str:
        """
        Converts a datetime.date object into a string in the format "MM/DD".
        """
        if isinstance(value, datetime.date):
            return value.strftime("%m/%d")  # noqa
        return value


class MonthDayInput(DateInput):
    """
    A custom date input widget that only displays the month and day fields.
    """

    input_type = "text"

    def __init__(self, **kwargs):
        self.format = kwargs.pop("format", "%m/%d")
        super().__init__(**kwargs)

    def format_value(self, value):
        if isinstance(value, datetime.date):
            return value.strftime(self.format)  # noqa
        return value


class MonthDayField(models.DateField):
    """
    A custom field that allows storing a month and day without the year.
    """

    def formfield(self, **kwargs):
        defaults = {"form_class": MonthDayFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    @staticmethod
    def from_db_value(value, expression, connection):
        """
        Converts the date string stored in the database into a datetime.date object.
        """
        if value is None:
            return None
        return parse_date(value)

    def get_prep_value(self, value):
        """
        Converts a datetime.date object into a string in the format "MM/DD".
        """
        if value is None:
            return None
        return value.strftime("%m/%d")

    def to_python(self, value):
        """
        Parses a string value representing a month/day date into a datetime.date
        object with the current year.
        """
        if not value:
            return None
        try:
            month, day = value.split("/")
            return (
                datetime.now()
                .replace(year=datetime.now().year, month=int(month), day=int(day))
                .date()
            )
        except ValueError:
            raise ValidationError(_("Invalid date format (must be MM/DD)"))


class PositiveOneSmallIntegerField(PositiveIntegerRelDbTypeMixin, SmallIntegerField):
    description = _("Positive small integer")

    def get_internal_type(self):
        return "PositiveSmallIntegerField"

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "min_value": 1,
                **kwargs,
            }
        )


class SetField(models.TextField):
    __token = " "

    def __init__(self, *args, **kwargs):
        super(SetField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.__token)

    def get_db_prep_value(self, value, **kwargs):
        if not value:
            return
        if isinstance(value, str):
            return value # allow corruption
        assert isinstance(value, list) or isinstance(value, tuple), f"value must be list or tuple, not {type(value)}"
        return self.__token.join(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
