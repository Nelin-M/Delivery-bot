"""
This module for creating state feedback
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateReview(StatesGroup):
    """
    This class for creating state feedback
    """

    review_text = State()
