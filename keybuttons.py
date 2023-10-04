from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import types

import data


class SetTimeCallback(CallbackData, prefix="set_time"):
    time_index: int


time_inline_buttons = InlineKeyboardBuilder()

for index in range(0, 12):
    time_inline_buttons.button(text=data.times[index],
                               callback_data=SetTimeCallback(time_index=index).pack())

time_inline_buttons.adjust(2, 2)
