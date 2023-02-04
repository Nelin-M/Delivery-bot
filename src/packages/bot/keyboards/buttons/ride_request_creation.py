"""
This module represents ride request creation ReplyKeyboards
"""
import datetime

import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def handle_date(days: int):
    """
    This function returns the current date plus days
    """
    # todo: добавить в setting часовой пояс (по дефолту стоит часовой пояс системы)
    return datetime.datetime.now() + datetime.timedelta(days)


def str_button(days: int):
    """
    This function returns string to create a button
    """
    return (
        f"{handle_date(days).day if len(str(handle_date(days).day)) == 2 else '0' + str(handle_date(days).day)}."
        f"{handle_date(days).month if len(str(handle_date(days).month)) == 2 else '0' + str(handle_date(days).month)}"
    )


def get_date_keyboard():
    date_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(str_button(0)), KeyboardButton(str_button(1)), KeyboardButton(str_button(2))],
            [KeyboardButton(str_button(3)), KeyboardButton(str_button(4)), KeyboardButton(str_button(5))],
            [KeyboardButton(str_button(6)), KeyboardButton(str_button(7)), KeyboardButton(str_button(8))],
            [KeyboardButton("Отмена")],
        ],
        resize_keyboard=True,
    )
    return date_keyboard


keyboard_ok = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Отправить"), KeyboardButton("Редактировать")], [KeyboardButton("Отменить заявку")]],
    resize_keyboard=True,
)
keyboard_main_profile = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Мой автомобиль")]],
    resize_keyboard=True,
)
keyboard_terms_delivery = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Дальше")],
        [KeyboardButton("За шоколадку " + emoji.emojize(":chocolate_bar:"))],
        # todo: вынести кнопку отмена и добавлять её с помощью метода add()
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)
keyboard_place_departure = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="ул.Звездова 101 A")], [KeyboardButton("Отмена")]],
    resize_keyboard=True,
)

default_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Отмена")]],
    resize_keyboard=True,
)
number_of_seats_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("1"), KeyboardButton("2")],
        [KeyboardButton("3"), KeyboardButton("4")],
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)
time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("23:15"), KeyboardButton("00:45"), KeyboardButton("01:15")],
        [KeyboardButton("02:15"), KeyboardButton("07:15"), KeyboardButton("08:15")],
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)
yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Да"), KeyboardButton("Не прикреплять ссылку")], [KeyboardButton("Изменить адрес")]],
    resize_keyboard=True,
)
