from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import types

import data
from date_and_hours import plus_day_to_current_time


class SetTimeCallback(CallbackData, prefix="set_time"):
    time_index: int
    day: int


def get_times_markup(day: int, busy_times):
    time_inline_buttons = InlineKeyboardBuilder()
    for index in range(len(data.times)):
        if index not in busy_times:
            time_inline_buttons.button(text=data.times[index],
                                       callback_data=SetTimeCallback(time_index=index, day=day).pack())

    time_inline_buttons.adjust(2, 2)

    return time_inline_buttons


class ChoseDayCallbackData(CallbackData, prefix="set_day"):
    day_delta: int


def get_days_markup():
    day_inline_buttons = InlineKeyboardBuilder()

    for i, day in enumerate(data.day_deltas):
        chosen_day = plus_day_to_current_time(i)
        day_inline_buttons.button(text=day + f"({datetime.fromtimestamp(chosen_day).strftime('%d %b')})",
                                  callback_data=ChoseDayCallbackData(day_delta=i))

    day_inline_buttons.adjust(1)
    return day_inline_buttons
