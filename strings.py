from aiogram.utils.markdown import hlink

import data
import sqlite_db


async def order_to_string_with_id(order):
    strings = []
    for row in order:
        tg_username, tg_name, time_index, day, tg_id = row
        strings.append(
            f'{tg_id} {tg_name} {await sqlite_db.get_name_and_block_by_id(tg_id)} {data.times[time_index]}')

    return '\n'.join(strings)


async def order_to_string(order, current_user_id):
    strings = []
    for row in order:
        tg_username, tg_name, time_index, day, tg_id = row
        if tg_id == current_user_id:
            strings.append(
                f'{hlink(await sqlite_db.get_name_and_block_by_id(tg_id), f"https://t.me/{tg_username}")}  {data.times[time_index]} ')
        else:
            strings.append(
                f'{hlink(await sqlite_db.get_name_and_block_by_id(tg_id), f"https://t.me/{tg_username}")} {data.times[time_index]}')

    return '\n'.join(strings)


def get_users_to_string(users, current_user_id):
    strings = []
    for row in users:
        tg_id, tg_username, block = row
        tg_username = str(tg_username)
        if tg_id == current_user_id:
            strings.append(f'{hlink("ты", f"https://t.me/{tg_username}")} {tg_id} комната {block}')
        else:
            strings.append(f'{hlink(tg_username, f"https://t.me/{tg_username}")} {tg_id} комната {block}')

    return '\n'.join(strings)
