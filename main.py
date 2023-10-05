import asyncio
import logging
import os
import sys

from aiogram.fsm.context import FSMContext

import data

import keybuttons
import sqlite_db
from aiogram.types import CallbackQuery
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from date_and_hours import get_current_hour, plus_day_to_current_time, get_busy_times_by_hour
from states import GettingRoomNumber
from strings import order_to_string

# Bot token can be obtained via https://t.me/BotFather


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
        # in_order = False
        if is_registred and not in_order:
            await message.answer("выберите день", reply_markup=keybuttons.day_inline_buttons.as_markup())
        elif in_order:
            await message.answer("ты уже в очереди")
        else:
            await message.answer("Вас нет в базе. Зарегайся")
    except TypeError:
        await message.answer("error order")


@dp.callback_query(keybuttons.ChoseDayCallbackData.filter())
async def show_free_times(query: CallbackQuery, callback_data: keybuttons.ChoseDayCallbackData):
    busy_times = await sqlite_db.get_busy_times(plus_day_to_current_time(callback_data.day_delta))
    if callback_data.day_delta == 0:
        busy_times = busy_times.union(get_busy_times_by_hour(get_current_hour()))
    await query.message.answer(f"выберите время на {data.day_deltas[callback_data.day_delta].lower()}",
                               reply_markup=keybuttons.get_times_markup(day=callback_data.day_delta,
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
            kb = [
                [
                    types.KeyboardButton(text="Запись"),
                    types.KeyboardButton(text="Очередь"),
                    # types.KeyboardButton(text="Регистрация"),
                    types.KeyboardButton(text="Уйти с очереди")
                ],
            ]
            await message.answer("ты успешно зареган",
                                 reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

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


@dp.message(F.text == "Очередь")
async def print_order(message: types.Message):
    try:
        is_busy = False
        for i in range(len(data.day_deltas)):
            order = await sqlite_db.get_orger_for_day(plus_day_to_current_time(i))
            if order:
                is_busy = True
                await message.answer(
                    f"{data.day_deltas[i]}\n" + order_to_string(order, message.from_user.username),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)
        if not is_busy:
            await message.answer("очередь пустая")

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
    await message.answer("Выберите номер комнаты(например 12.4.3)",
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
            # types.KeyboardButton(text="Регистрация"),
            types.KeyboardButton(text="Уйти с очереди")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Добро пожаловать в стиралку 12 этажа", reply_markup=keyboard)


@dp.callback_query(keybuttons.SetTimeCallback.filter())
async def set_time(query: CallbackQuery, callback_data: keybuttons.SetTimeCallback):
    message = query.message
    await sqlite_db.create_new_record(tg_username=message.chat.username,
                                      user_name=message.chat.first_name,
                                      day=plus_day_to_current_time(callback_data.day),
                                      time_index=callback_data.time_index)
    await query.message.answer(
        f"Вы записаны {data.day_deltas[callback_data.day]} {data.times[callback_data.time_index]}")
    await query.answer()


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer("а??")
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    from aiogram.client.session.aiohttp import AiohttpSession
    session = AiohttpSession(proxy="http://proxy.server:3128")

    bot = Bot(TOKEN, session=session, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
    await sqlite_db.db_connect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
