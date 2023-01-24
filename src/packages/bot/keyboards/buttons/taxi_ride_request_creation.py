from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_terms_delivery_taxi = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Стоимость поездки распределяется между всеми участниками")],
        [KeyboardButton("Дальше")],
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)
