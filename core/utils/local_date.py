import datetime
from itertools import islice

from django.utils import timezone


def get_localdate(date=None, time=None):
    if date is None:
        date = timezone.localdate()
    if time is not None:
        date = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time(*time))
        )
    return date


def generate_years():
    current_year = timezone.now().year
    year_ranges = [
        f"{year}-{str(year + 1)[-2:]}" for year in range(2021, current_year + 2)
    ]
    years = zip(year_ranges, year_ranges)
    return list(years)
