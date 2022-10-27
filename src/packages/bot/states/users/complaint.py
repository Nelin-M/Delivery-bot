"""
This module for creating state complaint
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateComplaint(StatesGroup):
    """
    This class for creating state complaint
    """

    complaint_text = State()
