import datetime

from django.utils import timezone


def get_localdate(date=None, time=None):
    if date is None:
        date = timezone.localdate()
    if time is not None:
        date = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time(*time))
        )
    return date
