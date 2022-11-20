"""
This module keeps car profile FSMs
"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class EditCarFSM(StatesGroup):
    """
    Finite state machine to lead user making him fill info about his car
    """

    brand = State()
    model = State()
    number_plate = State()
    confirmation = State()
    result_handling = State()


class DeleteCarFSM(StatesGroup):
    """
    Finite state machine to lead user making him confirm delete intention
    """

    confirmation = State()
