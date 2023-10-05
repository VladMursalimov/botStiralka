from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import types

import data


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


day_inline_buttons = InlineKeyboardBuilder()

for i, day in enumerate(data.day_deltas):
    day_inline_buttons.button(text=day, callback_data=ChoseDayCallbackData(day_delta=i))
