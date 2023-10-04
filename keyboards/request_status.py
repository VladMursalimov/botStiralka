from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

request_status_captions = ["Одобрить", "Отклонить", "◀ Назад"]

request_status = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=request_status_captions[0]),
         KeyboardButton(text=request_status_captions[1])],
        [KeyboardButton(text=request_status_captions[2])]],
    resize_keyboard=True)
