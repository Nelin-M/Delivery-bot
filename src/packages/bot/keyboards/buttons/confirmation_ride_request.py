"""
Keyboard for the confirmation ride request
"""
from aiogram import types

button_cancel = types.KeyboardButton(text="Отмена")
keyboard_ok = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_requests_ok = types.KeyboardButton(text="Отправить")
button_menu = types.KeyboardButton(text="В главное меню")
button_requests_error = types.KeyboardButton(text="Отменить заявку")
keyboard_ok.add(button_requests_ok)
keyboard_ok.add(button_requests_error)
keyboard_ok.add(button_menu)
