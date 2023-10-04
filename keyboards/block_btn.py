from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

block_btn_captions = ["12.1", "12.2", "12.3", "12.4",
                      "12.5", "12.6", "12.7", "12.8",
                      "Назад"]

block_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=block_btn_captions[0]),
         KeyboardButton(text=block_btn_captions[1]),
         KeyboardButton(text=block_btn_captions[2]),
         KeyboardButton(text=block_btn_captions[3]), ],
        [KeyboardButton(text=block_btn_captions[4]),
         KeyboardButton(text=block_btn_captions[5]),
         KeyboardButton(text=block_btn_captions[6]),
         KeyboardButton(text=block_btn_captions[7])],
        [KeyboardButton(text=block_btn_captions[8])]],
    resize_keyboard=True)
