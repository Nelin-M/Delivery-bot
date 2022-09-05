"""
Keyboard for the input departure place
"""
from aiogram import types

button_cancel = types.KeyboardButton(text="Отмена")
keyboard_place_departure = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_place_departure = types.KeyboardButton(text="ул.Звездова 101 A")
keyboard_place_departure.add(button_place_departure)
keyboard_place_departure.add(button_cancel)
