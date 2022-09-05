"""
Keyboard for the input delivery_terms
"""
from aiogram import types
import emoji

button_cancel = types.KeyboardButton(text="Отмена")
keyboard_terms_delivery = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_terms_delivery = types.KeyboardButton(text="Дальше")
button_shoko = types.KeyboardButton(text="За шоколадку " + emoji.emojize(":chocolate_bar:"))
keyboard_terms_delivery.add(button_shoko)
keyboard_terms_delivery.add(button_terms_delivery)
keyboard_terms_delivery.add(button_cancel)
