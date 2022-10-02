import pytz

timezone_choices = [(i, i) for i in pytz.common_timezones]

graduating_year_choices = [
    (None, "Does not apply"),
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
]

announcement_status_choices = [
    ("d", "Draft"),
    ("p", "Pending Approval"),
    ("a", "Approved"),
    ("r", "Rejected"),
]
