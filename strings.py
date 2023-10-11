from aiogram.utils.markdown import hlink

import data


def order_to_string(order, current_user_id):
    strings = []
    for row in order:
        tg_username, tg_name, time_index, day, tg_id = row
        if tg_id == current_user_id:
            strings.append(f'{hlink("ты", f"https://t.me/{tg_username}")}  {data.times[time_index]} ')
        else:
            strings.append(f'{hlink(tg_name, f"https://t.me/{tg_username}")} {data.times[time_index]}')

    return '\n'.join(strings)


def get_users_to_string(users, current_user_id):
    strings = []
    for row in users:
        tg_id, tg_username, block = row
        tg_username = str(tg_username)
        if tg_id == current_user_id:
            strings.append(f'{hlink("ты", f"https://t.me/{tg_username}")}  комната {block}')
        else:
            strings.append(f'{hlink(tg_username, f"https://t.me/{tg_username}")} комната {block}')

    return '\n'.join(strings)
