"""
This module is responsible for loading the configuration file for the bot and loading the environment variables.
"""

from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


#
def setup(dispatcher: Dispatcher):
    """
    Installing anti-spam for a bot
    @param dispatcher: dispatcher
    """

    dispatcher.middleware.setup(ThrottlingMiddleware())
