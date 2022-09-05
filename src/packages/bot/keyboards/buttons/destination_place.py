"""
Keyboard for the input destination place
"""
from aiogram import types

button_cancel = types.KeyboardButton(text="Отмена")
default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add(button_cancel)
