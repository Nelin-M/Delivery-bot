"""
Keyboard for the main menu
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_authorised = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Создать заявку"), KeyboardButton("Такси"), KeyboardButton("Мои заявки")],
        [KeyboardButton("Мой автомобиль"), KeyboardButton("Обратная связь"), KeyboardButton("Пожаловаться")],
        [KeyboardButton("Назад")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


main_menu_unauthorised = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Создать профиль")]], resize_keyboard=True, one_time_keyboard=True
)
