import asyncio
import datetime
import logging
import os
import sys
from os import getenv

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

import data

import keybuttons
import sqlite_db
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from states import GettingRoomNumber

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("bot_token")
router = Router()
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(F.text == "Запись")
async def take_part_in_order(message: types.Message):
    try:
        is_registred = await sqlite_db.check_user(message.from_user.id)
        in_order = await sqlite_db.is_in_order(message.from_user.username)
        if is_registred and not in_order:
            await message.answer("выберите день", reply_markup=keybuttons.day_inline_buttons.as_markup())
        elif in_order:
            await message.answer("ты уже в очереди")
        else:
            await message.answer("Вас нет в базе. Зарегайся")
    except TypeError:
        await message.answer("error order")


def get_current_day():
    return datetime.datetime.now().day


@dp.callback_query(keybuttons.ChoseDayCallbackData.filter())
async def show_free_times(query: CallbackQuery, callback_data: keybuttons.ChoseDayCallbackData):
    busy_times = await sqlite_db.get_busy_times(get_current_day() + callback_data.day)
    await query.message.answer("выберите время",
                               reply_markup=keybuttons.get_times_markup(day=callback_data.day,
                                                                        busy_times=busy_times).as_markup())
    await query.answer()


@dp.message(GettingRoomNumber.getting_number)
async def register_with_room(message: types.Message, state: FSMContext):
    try:
        is_registred = await sqlite_db.check_user(message.from_user.id)
        if is_registred:
            await message.answer("ты уже зареган")
        else:
            await sqlite_db.register_new_user(message.from_user.id, message.from_user.username, message.text)
            await message.answer("ты успешно зареган")

    except TypeError:
        await message.answer("error register")
    await state.clear()


@dp.message(F.text == "Регистрация")
async def register(message: types.Message):
    try:
        is_registred = await sqlite_db.check_user(message.from_user.id)
        if is_registred:
            await message.answer("ты уже зареган")
        else:
            await sqlite_db.register_new_user(message.from_user.id, message.from_user.username, "0.0.0")
            await message.answer("ты успешно зареган")

    except TypeError:
        await message.answer("error register")


def order_to_string(order):
    strings = []
    for row in order:
        tg_username, tg_name, time_index = row
        strings.append(f"@{tg_username} {tg_name} {data.times[time_index]}")

    return '\n'.join(strings)


@dp.message(F.text == "Очередь")
async def print_order(message: types.Message):
    try:
        order = await sqlite_db.get_order()
        await message.answer(order_to_string(order))
    except TypeError:
        await message.answer("error")


@dp.message(F.text == "Уйти с очереди")
async def out_of_order(message: types.Message):
    try:
        if await sqlite_db.is_in_order(message.from_user.username):
            await sqlite_db.delete_from_order(message.from_user.username)
            await print_order(message)
        else:
            await message.answer("вас нет в очереди")
    except TypeError:
        await message.answer("error")


async def ask_to_block_number(message: types.Message, state: FSMContext):
    await state.set_state(GettingRoomNumber.getting_number)

    kb = [
        [
            types.KeyboardButton(text="отмена"),
        ],
    ]
    await message.answer("Введите номер комнаты(например 12.4.3)",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))


@dp.message(F.text == "отмена")
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await send_welcome(message, state)


@dp.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    is_registred = await sqlite_db.check_user(message.from_user.id)

    if not is_registred:
        await ask_to_block_number(message, state)
        return

    kb = [
        [
            types.KeyboardButton(text="Запись"),
            types.KeyboardButton(text="Очередь"),
            types.KeyboardButton(text="Регистрация"),
            types.KeyboardButton(text="Уйти с очереди")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("привет", reply_markup=keyboard)


@dp.callback_query(keybuttons.SetTimeCallback.filter())
async def set_time(query: CallbackQuery, callback_data: keybuttons.SetTimeCallback):
    message = query.message
    await sqlite_db.create_new_record(message.chat.username, message.chat.first_name, callback_data.day)
    await query.message.answer(f"Вы записаны на {data.times[callback_data.time_index]}")
    await print_order(message)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer("а??")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)
    await sqlite_db.db_connect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
