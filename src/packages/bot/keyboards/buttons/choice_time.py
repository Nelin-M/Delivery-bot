"""
Keyboard for the choice time
"""
from aiogram import types

button_cancel = types.KeyboardButton(text="Отмена")
time_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
time_keyboard.row(*["22:00", "22:10", "22:20", "22:30", "22:40"])
time_keyboard.row(*["23:00", "23:10", "23:20", "23:30", "23:40"])
time_keyboard.row(*["01:00", "01:10", "01:20", "01:30", "01:40"])
time_keyboard.row(*["02:00", "02:10", "02:20", "02:30", "02:40"])
time_keyboard.add(button_cancel)
