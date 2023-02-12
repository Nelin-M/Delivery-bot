from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.packages.bot.other.Utils import str_button
from src.packages.loaders import env_variables

"""
Utils buttons
"""


def create_keyboard(buttons_name, lines, cancel_button=False):
    """
    This function generate list KeyboardButtons
    """
    keyboard = []
    keyboard_temp = []
    for name in buttons_name:
        keyboard_temp.append(KeyboardButton(name))
        if len(keyboard_temp) == lines:
            keyboard.append(keyboard_temp.copy())
            keyboard_temp.clear()
    if keyboard_temp and "" not in keyboard_temp:
        keyboard.append(keyboard_temp.copy())
    if cancel_button:
        keyboard.append([KeyboardButton("Отмена")])
    return keyboard


def ReplyResizeKeyboardAndOneTimeList(buttons_name, lines=2, cancel_button=False):
    """
    This function returns ReplyKeyboardMarkup with params
    resize_keyboard = True
    one_time_keyboard = True
    """
    return ReplyKeyboardMarkup(
        keyboard=create_keyboard(buttons_name, lines, cancel_button),
        resize_keyboard=True,
        one_time_keyboard=True)


def ReplyResizeKeyboardList(buttons_name, lines=2, cancel_button=False):
    """
    This function returns ReplyKeyboardMarkup with params
    resize_keyboard = True
    """
    return ReplyKeyboardMarkup(
        keyboard=create_keyboard(buttons_name, lines, cancel_button),
        resize_keyboard=True)


def InlineKeyboardList(buttons_name, lines=2, cancel_button=False):
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оставить отзыв", callback_data="Оставить отзыв"),
                InlineKeyboardButton(text="Посмотреть отзывы", url=channel_feedback_link),
            ]
        ],
    )


def get_date_keyboard():
    """
    This function returns dates in list
    range(0,9) - means that from 0 element to 9
    """
    date_keyboard = ReplyResizeKeyboardList([str_button(i) for i in range(0, 9)],
                                            3, cancel_button=True)
    return date_keyboard
