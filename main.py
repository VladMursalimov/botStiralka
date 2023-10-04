import asyncio
import logging
import sys

from keyboards.request_status import *
from sqlite_db import *
from aiogram import Bot, Dispatcher, types, F
# ------------------
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.filters import CommandObject
# ------------------
from aiogram.types import Message
# ----------------------
# from config import config
from data import config
# import keyboards
from keyboards.main_menu import *
from keyboards.admin_menu import *
from keyboards.admin_commands import *
from keyboards.block_btn import *
# --------------



dp = Dispatcher()

@dp.message(F.text == main_captions[0] or F.text == main_admin_captions[0])
async def new_in_order(message: Message):
    try:
        # проверка на регистрацию
        is_registred = await check_user(message.from_user.id)
        # проверка на очередь
        in_order = await is_in_order(message.from_user.username)
        # если ты зареган и не в очереди
        if is_registred and not in_order:
            # добавляем тебя в очередь
            await create_new_record(message.from_user.username,
                                    message.from_user.first_name, message.date)
            # выводим очередь
            await print_order(message)
        # уже в очереди
        elif in_order:
            await message.answer("ты уже в очереди")
        # нет ни в очереди, ни в базе
        else:
            await message.answer("Вас нет в базе. Зарегайся")
    except TypeError:
        await message.answer("Ошибка в записи, обратитесь к админу")


# РЕГИСТРАЦИЯ---------------------------------
@dp.message(F.text == main_captions[2] or F.text == main_admin_captions[2])
async def register(message: Message):
    try:
        is_base_user = await check_user(message.from_user.id)
        is_send_request = await check_user_request(message.from_user.id)
        if is_send_request:
            await message.answer("Ты уже подал заявку")
        elif is_base_user:
            await message.answer("Ты зареган")
        else:
            await get_key(message)
    except TypeError:
        await message.answer("Ошибка регистрации, обратитесь к админу")


async def get_key(message: Message):
    await message.answer(f"Выбери блок", reply_markup=block_btn)
    return 1


@dp.message(F.text == block_btn_captions[0])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.1",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[1])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.2",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[2])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.3",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[3])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.4",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[4])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.5",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[5])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.6",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[6])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.7",
                          message.date)
        await message.answer("Заявка отправлена")


@dp.message(F.text == block_btn_captions[7])
async def register_block_0(message: Message):
    if get_key(message):
        await add_request(message.from_user.id,
                          message.from_user.username,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          "12.8",
                          message.date)
        await message.answer("Заявка отправлена")


# ---------------------------------
# @dp.message(F.text == main_captions[2] or F.text == main_admin_captions[2])
# async def register(message: Message):
#     try:
#         is_registred = await check_user(message.from_user.id)
#         if is_registred:
#             await message.answer("Ты уже зарегистрировался")
#         else:
#             await register_new_user(message.from_user.id,
#                                     message.from_user.username, "12.4")
#             await message.answer("Ты успешно зарегистрировался")
#
#     except TypeError:
#         await message.answer("Ошибка регистрации, обратитесь к админу")


def order_to_string(order):
    strings = []
    for index, row in enumerate(order):
        tg_username, tg_name, time = row
        strings.append(f"{index + 1}) @{tg_username} {tg_name} {time}")

    return '\n'.join(strings)


@dp.message(F.text == main_captions[1] or F.text == main_admin_captions[1])
async def print_order(message: Message):
    try:
        order = order_to_string(await get_order())
        if order:
            await message.answer(order)
        else:
            await message.answer("Стиральная машина свободна")

    except TypeError:
        await message.answer("print_order error")


@dp.message(F.text == main_captions[3] or F.text == main_admin_captions[3])
async def out_of_order(message: Message):
    try:
        if await is_in_order(message.from_user.username):
            await delete_from_order(message.from_user.username)
            await print_order(message)
        else:
            await message.answer("Вас нет в очереди")
    except TypeError:
        await message.answer("out_of_order error")


@dp.message(F.text == main_admin_captions[4])
async def admin_panel(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            await message.answer("Панель Администратора", reply_markup=admin_commands)
    except TypeError:
        await message.answer("admin_panel - error")


# ---- MANAGE ADMIN--------
def request_to_string(request):
    for row in request:
        return row


# Заявки
@dp.message(F.text == admin_commands_captions[0])
async def admin_request(message: Message):
    # try:
    if message.from_user.id == int(config.ADMIN_ID):
        request = await get_requests()
        requests_string = request_to_string(request)
        if requests_string == None:
            await message.answer('Заявок нет')
        else:
            print('------------>', requests_string)
            requests_string_1 = ''
            for i in requests_string:
                if i != None:
                    requests_string_1 += ' ' + str(i)
            await message.answer(f'{1}) ' + requests_string_1,
                                 reply_markup=request_status)


# except TypeError:
#     await message.answer("admin_request - error!!!")


# Создать объявление
@dp.message(F.text == admin_commands_captions[1])
async def admin_create_advertisement(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            await message.answer("Напишите объявление: не забудь добавить /admin_ad")
    except TypeError:
        await message.answer("admin_create_advertisement - error!!!")


# Отправить объявление
@dp.message(Command("admin_ad"))
async def admin_send_ad(message: types.Message, command: CommandObject):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            if command.args:
                users = await get_user()
                for i in users:
                    print(i)
                    await bot.send_message(chat_id=i[0],
                                           text=f"Объявление:\n{command.args}")
            else:
                await message.answer("Пожалуйста, укажи объявление после команды /admin_ad!")

    except TypeError:
        await message.answer("admin_send_ad - error!!!")


# База студентов
@dp.message(F.text == admin_commands_captions[5])
async def admin_base_users(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            users = await get_user()
            for indx, i in enumerate(users):
                tg_id, tg_name, block = i
                await message.answer(f"{indx}) @{tg_name} {block}")

    except TypeError:
        await message.answer("admin_send_ad - error!!!")


# Одобрить
@dp.message(F.text == request_status_captions[0])
async def accept_request(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            request = request_to_string(await get_requests())
            if request:
                tg_id, tg_username, user_name, user_lastname, block, time = request
                await register_new_user(tg_id, tg_username, block)
                await delete_from_requests(tg_username)
                await message.answer("Панель Администратора", reply_markup=admin_commands)
            else:
                print('очередь пуста')
    except TypeError:
        await message.answer('accept_request error')


# Отклонить
@dp.message(F.text == request_status_captions[1])
async def fatal_request(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            request = request_to_string(await get_requests())
            if request:
                tg_id, tg_username, user_name, user_lastname, block, time = request
                await delete_from_requests(tg_username)
                await message.answer("Панель Администратора", reply_markup=admin_commands)
            else:
                print('очередь пуста')
    except TypeError:
        await message.answer("fatal_request error")


# Назад к панели админа
@dp.message(F.text == request_status_captions[2])
async def admin_back_to_admin_commands(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            await message.answer("Панель Администратора", reply_markup=admin_commands)
    except TypeError:
        await message.answer("admin_back_to_admin_commands error")


# Назад в глаавное меню
@dp.message(F.text == admin_commands_captions[4])
async def admin_back_to_main_menu(message: Message):
    try:
        if message.from_user.id == int(config.ADMIN_ID):
            await message.answer("Выберите параметры", reply_markup=admin_menu)
    except TypeError:
        await message.answer("admin_back_to_main_menu")


# --------------------------------

@dp.message(CommandStart())
async def send_welcome(message: Message):
    if message.from_user.id == int(config.ADMIN_ID):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=admin_menu)
    else:
        await message.answer("Добро пожаловать в бота для записи на стирку", reply_markup=main_menu)


@dp.message()
async def echo_handler(message: Message):
    try:
        await message.answer("a??")
    except TypeError:
        await message.answer("Nice try!")


async def main():
    global bot
    # Initialize Bot instance with a default parse mode
    # which will be passed to all API calls
    bot = Bot(token=config.BOT_TOKEN)



    # And the run events dispatching
    await dp.start_polling(bot)
    await db_connect()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
