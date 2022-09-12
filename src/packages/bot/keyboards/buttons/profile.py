"""
This module represents user profile ReplyKeyboards
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


profile_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Редактировать профиль"), KeyboardButton("Мой автомобиль")],
        [KeyboardButton("Удалить профиль"), KeyboardButton("Назад")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profile_delete_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Да"), KeyboardButton("Отменить")]], resize_keyboard=True, one_time_keyboard=True
)


profile_data_confirmation = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Всё верно"), KeyboardButton("Хочу исправить")], [KeyboardButton("Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
