from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_captions = ["🔴 Запись",
                 "📤 Очередь",
                 "✍🏼 Регистрация",
                 "🚩️ Уйти с очереди",
                       "🛠️ Админ"]

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=main_admin_captions[0]),
         KeyboardButton(text=main_admin_captions[4])],
        [KeyboardButton(text=main_admin_captions[1]),
         KeyboardButton(text=main_admin_captions[2])],
        [KeyboardButton(text=main_admin_captions[3])],],
    resize_keyboard=True)
