"""
This module keeps profile FSMs
"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class EditProfileFSM(StatesGroup):
    """
    Finite state machine to lead user making him fill info about himself
    """

    first_name = State()
    last_name = State()
    phone_number = State()
    confirmation = State()
    result_handling = State()


class DeleteProfileFSM(StatesGroup):
    """
    Finite state machine to lead user making him confirm delete intention
    """

    confirmation = State()
