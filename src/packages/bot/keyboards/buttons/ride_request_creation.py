"""
This module represents ride request creation ReplyKeyboards
"""
import datetime
import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def handle_date(days):
    """
    This function returns the current date plus days
    @param days: int
    """
    return datetime.datetime.now() + datetime.timedelta(days)


def str_button(days):
    """
    This function returns string to create a button
    @param days: int
    """
    return (
        f"{handle_date(days).day if len(str(handle_date(days).day)) == 2 else '0' + str(handle_date(days).day)}."
        f"{handle_date(days).month if len(str(handle_date(days).month)) == 2 else '0' + str(handle_date(days).month)}"
    )


date_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(str_button(1)), KeyboardButton(str_button(2)), KeyboardButton(str_button(3))],
        [KeyboardButton(str_button(4)), KeyboardButton(str_button(5)), KeyboardButton(str_button(6))],
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)

time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("22:00"),
            KeyboardButton("22:10"),
            KeyboardButton("22:20"),
            KeyboardButton("22:30"),
            KeyboardButton("22:40"),
        ],
        [
            KeyboardButton("23:00"),
            KeyboardButton("23:10"),
            KeyboardButton("23:20"),
            KeyboardButton("23:30"),
            KeyboardButton("23:40"),
        ],
        [
            KeyboardButton("00:00"),
            KeyboardButton("00:10"),
            KeyboardButton("00:20"),
            KeyboardButton("00:30"),
            KeyboardButton("00:40"),
        ],
        [
            KeyboardButton("01:00"),
            KeyboardButton("01:10"),
            KeyboardButton("01:20"),
            KeyboardButton("01:30"),
            KeyboardButton("01:40"),
        ],
        [KeyboardButton("Отмена")],
    ],
    resize_keyboard=True,
)

keyboard_ok = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Отправить")], [KeyboardButton("Отменить заявку")]],
    resize_keyboard=True,
)

keyboard_terms_delivery = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Дальше")],
        [KeyboardButton("За шоколадку " + emoji.emojize(":chocolate_bar:"))],
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
