"""
Inline keyboard for the feedback group
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

add_car_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Добавить автомобиль", callback_data="Добавить автомобиль")]],
)
