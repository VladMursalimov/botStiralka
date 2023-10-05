import datetime

import data

from zoneinfo import ZoneInfo

import sqlite_db

time_zone = ZoneInfo('Europe/Moscow')


def plus_day_to_current_time(day):
    return int((datetime.timedelta(days=day) + get_current_datetime()).timestamp())


def get_current_hour():
    # return 13
    return get_current_datetime().hour


def get_current_week():
    return get_current_datetime().weekday()


def get_current_day():
    return int(get_current_datetime().timestamp())


def get_current_datetime():
    now = datetime.datetime.now(time_zone).replace(second=0, microsecond=0, minute=0)
    return now


def get_busy_times_after_hour(busy_times):
    busy_times_t = set()
    for busy_time_index in busy_times:
        busy_times_t.add(busy_time_index + 1)
        busy_times_t.add(busy_time_index + 2)
        busy_times_t.add(busy_time_index - 1)
        busy_times_t.add(busy_time_index - 2)
    return busy_times_t


def get_busy_times_by_hour(hour):
    print(hour)
    busy_times = set()
    for i in range(len(data.times_hours)):
        if hour >= data.times_hours[i]:
            busy_times.add(i)
    return busy_times
