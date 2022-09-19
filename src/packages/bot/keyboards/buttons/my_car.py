"""
This module represents car profile ReplyKeyboards
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

add_car_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Добавить автомобиль")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

car_added_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Редактировать автомобиль"), KeyboardButton("Удалить автомобиль")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

car_create_confirmation_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Всё верно"), KeyboardButton("Хочу исправить")], [KeyboardButton("Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

car_delete_confirmation = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Да"), KeyboardButton("Отменить")]], resize_keyboard=True, one_time_keyboard=True
)
