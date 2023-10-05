import datetime


def plus_day_to_current_time(day):
    return int((datetime.timedelta(days=day) + get_current_datetime()).timestamp())


def get_current_hour():
    return datetime.datetime.now().hour


def get_current_week():
    return datetime.datetime.now().weekday()


def get_current_datetime():
    now = datetime.datetime.now().replace(second=0, microsecond=0, minute=0)
    return now
