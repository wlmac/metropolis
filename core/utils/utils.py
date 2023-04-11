from datetime import datetime


def get_week_and_day(dt: datetime.date):
    week_num = (dt.day - 1) // 7 + 1
    day_num = dt.weekday()
    return week_num, day_num


daysPerMonth = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}
