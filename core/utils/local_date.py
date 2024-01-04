from __future__ import annotations

import datetime
from typing import List, Literal, Tuple, Optional

from django.utils import timezone


def get_localdate(date=None, time=None):
    if date is None:
        date = timezone.localdate()
    if time is not None:
        date = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time(*time))
        )
    return date


def calculate_years(
    fmt: Literal["generate", "is_alumni"], user_years: Optional[List] = None
) -> List[Tuple[str, str]] | bool:
    if fmt == "is_alumni" and user_years is None:
        raise ValueError("user_years must be provided when fmt is is_alumni")

    current_year = timezone.now().year
    current_month = timezone.now().month

    # If the current month is between January and July, use the previous year
    if 1 <= current_month <= 7:
        current_year -= 1
    if fmt == "generate":
        year_ranges = [
            f"{year}-{str(year + 1)}"
            for year in range(2021, current_year + 2)  # generate next years to
        ]
        years = zip(year_ranges, year_ranges)
        return list(years)
    elif fmt == "is_alumni":
        current_year_range = f"{current_year}-{str(current_year + 1)}"
        return current_year_range not in user_years
