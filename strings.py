from aiogram.utils.markdown import hlink

import data


def order_to_string(order, current_user_id):
    strings = []
    for row in order:
        tg_username, tg_name, time_index, day, tg_id = row
        if tg_id == current_user_id:
            strings.append(f'{hlink("ты", f"https://t.me/{tg_username}")} {data.times[time_index]}')
        else:
            strings.append(f'{hlink(tg_name, f"https://t.me/{tg_username}")} {data.times[time_index]}')

    return '\n'.join(strings)


def get_day_string(day, month):
    months_names = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "август", "сентября", "октября",
                    "ноября", "декабря"]

    return f"{day} {months_names[month]}"

