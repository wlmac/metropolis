from __future__ import annotations

from typing import Literal, Optional, List, Tuple

import pytz
from django.utils import timezone

timezone_choices = [(i, i) for i in pytz.common_timezones]

announcement_status_choices = [
    ("d", "Draft"),
    ("p", "Pending Approval"),
    ("a", "Approved"),
    ("r", "Rejected"),
]

announcement_status_initial_choices = [
    ("d", "Draft (don't send)"),
    ("p", "Send to supervisor for review"),
]


def calculate_student_years() -> List[Tuple[int | str, int | None]]:
    current_year = timezone.now().year
    current_month = timezone.now().month

    # If the current month is between January and July, use the previous year
    if current_month >= 9:
        current_year += 1
    year_ranges = [
        (year, year)
        for year in range(current_year, current_year + 4)  # generate next years to
    ]
    year_ranges.insert(0, (None, "Does not apply"))
    return year_ranges


graduating_year_choices = calculate_student_years()


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
