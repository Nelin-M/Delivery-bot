"""
Setup class in middleware
"""

from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup_middleware(dispatcher: Dispatcher):
    """
    Installing anti-spam for a bot
    @param dispatcher: dispatcher
    """

    dispatcher.middleware.setup(ThrottlingMiddleware())
