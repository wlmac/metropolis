import pytz

timezone_choices = [(i, i) for i in pytz.common_timezones]

graduating_year_choices = [
    (None, "Does not apply"),
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
    (2027, 2027),
]

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
