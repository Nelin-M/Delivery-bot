"""
This module for creating state taxi ride request
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateTaxiRideRequest(StatesGroup):
    """
    This class for creating state taxi ride request
    """

    date = State()
    time = State()
    delivery_terms = State()
    place_departure = State()
    place_comming = State()
    number_of_seats = State()
    author = State()
