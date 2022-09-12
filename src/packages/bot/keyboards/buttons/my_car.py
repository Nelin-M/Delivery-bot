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
