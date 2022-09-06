"""
Initialising users ReplyKeyboards
"""


from .main_menu import keyboards_main_menu
from .choice_date import date_keyboard
from .choice_time import time_keyboard
from .confirmation_ride_request import keyboard_ok
from .destination_place import default_keyboard
from .seats_number import number_of_seats_keyboard
from .delivery_terms import keyboard_terms_delivery
from .departure_place import keyboard_place_departure

__all__ = [
    "main_menu_authorised",
    "main_menu_unauthorised",
    "profile_menu",
    "profile_delete_menu",
    "profile_data_confirmation",
]
