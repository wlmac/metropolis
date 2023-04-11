from datetime import datetime


def get_week_and_day(dt: datetime.date):
    week_num = (dt.day - 1) // 7 + 1
    day_num = dt.weekday()
    return week_num, day_num


daysPerMonth = {'January', 31, 'February', 28, 31, 'March', 'April', 30, 31, 'May', 'June', 30, 'July', 31, 31,
                'August', 'September', 30, 'October', 31, 'November', 30, 'December', 31}


months = {1, 'January', 2, 'February', 3, 'March', 4, 'April', 5, 'May', 6, 'June', 7, 'July', 8, 'August', 9, 'September', 10, 'October', 11, 'November', 12, 'December'}

