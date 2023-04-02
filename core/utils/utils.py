from datetime import datetime


def get_week_and_day(dt: datetime.date):
    week_num = (dt.day - 1) // 7 + 1
    day_num = dt.weekday()
    return week_num, day_num
