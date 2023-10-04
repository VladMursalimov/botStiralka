from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_commands_captions = ["Заявки",
                           "Создать объявление",
                           "Удалить из базы",
                           "Очистить очередь",
                           "Назад",
                           "База студентов"]

admin_commands = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=admin_commands_captions[0]),
         KeyboardButton(text=admin_commands_captions[1])],
        [KeyboardButton(text=admin_commands_captions[5]),
         KeyboardButton(text=admin_commands_captions[3])],
        [KeyboardButton(text=admin_commands_captions[4]),
         KeyboardButton(text=admin_commands_captions[2])]],
    resize_keyboard=True)
