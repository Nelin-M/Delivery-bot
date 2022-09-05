"""
Keyboard for the input seats_number
"""
from aiogram import types

button_cancel = types.KeyboardButton(text="Отмена")
number_of_seats_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
number_of_seats_keyboard.row(*["1", "2"])
number_of_seats_keyboard.row(*["3", "4"])
number_of_seats_keyboard.add(button_cancel)
