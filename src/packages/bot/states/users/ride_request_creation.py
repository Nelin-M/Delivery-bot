"""
This module for creating state ride request
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateRideRequest(StatesGroup):
    """
    This class for creating state ride request
    """

    date = State()
    time = State()
    delivery_terms = State()
    place_departure = State()
    place_coming = State()
    place_departure_update = State()
    route_link = State()
    number_of_seats = State()
    driver = State()
