"""
Keyboard for the main menu
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_authorised = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Создать заявку"), KeyboardButton("Мои заявки"), KeyboardButton("Мой профиль")],
        [KeyboardButton("Обратная связь"), KeyboardButton("Назад")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


main_menu_unauthorised = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Создать профиль")]], resize_keyboard=True, one_time_keyboard=True
)
