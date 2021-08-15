import pytz

timezone_choices = [(i, i) for i in pytz.common_timezones]

graduating_year_choices = [
    (2022, 2022),
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
    (2027, 2027),
]

announcement_status_choices = [
    ("p", "Pending Approval"),
    ("a", "Approved"),
    ("r", "Rejected"),
]
