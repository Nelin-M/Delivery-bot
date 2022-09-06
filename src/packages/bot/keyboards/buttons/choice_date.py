"""
Keyboard for the choice date
"""
import datetime
from aiogram import types

date_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
month = datetime.datetime.now().month
day = datetime.datetime.now().day
COUNT_ITEM = 0
row = []

for i in range(day, day + 5):
    if COUNT_ITEM == 3:
        date_keyboard.row(*row)
        row.clear()
        COUNT_ITEM = 0
    STR_MONTH = str(month)
    STR_DAY = str(day)
    button = f"{i if len(STR_DAY) == 2 else '0' + str(i)}.{month if len(STR_MONTH) == 2 else '0' + STR_MONTH}"
    row.append(button)
    COUNT_ITEM += 1
date_keyboard.row(*row)
button_cancel = types.KeyboardButton(text="Отмена")
date_keyboard.add(button_cancel)
