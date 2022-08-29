"""
Keyboard for the main menu
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать/редактировать профиль")],
        [KeyboardButton(text="Создать заявку"), KeyboardButton(text="Мои заявки")],
        [KeyboardButton(text="Отзывы"), KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
