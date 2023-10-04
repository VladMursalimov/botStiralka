from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_captions = ["🔴 Запись",
                 "📤 Очередь",
                 "✍🏼 Регистрация",
                 "🚩️ Уйти с очереди"]

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=main_captions[0])],
        [KeyboardButton(text=main_captions[1])],
        [KeyboardButton(text=main_captions[2])],
        [KeyboardButton(text=main_captions[3])]],
    resize_keyboard=True)
