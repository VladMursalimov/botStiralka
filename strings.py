from aiogram.utils.markdown import hlink

import data


def order_to_string(order, current_user):
    strings = []
    for row in order:
        tg_username, tg_name, time_index, day = row
        if tg_username == current_user:
            strings.append(f'{hlink("ты", f"https://t.me/{tg_username}")} {data.times[time_index]}')
        else:
            strings.append(f'{hlink(tg_username, f"https://t.me/{tg_username}")} {data.times[time_index]}')

    return '\n'.join(strings)


def get_day_string(day, month):
    months_names = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "август", "сентября", "октября",
                    "ноября", "декабря"]

    return f"{day} {months_names[month]}"

