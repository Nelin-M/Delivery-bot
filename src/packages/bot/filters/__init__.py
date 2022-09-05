"""
Initializing modules
"""

from aiogram import Dispatcher
from .users import ChatWithABot, GroupMember, AuthorisedUser


def setup_filters(dispatcher: Dispatcher):
    """
    Registration of filters
    """

    dispatcher.filters_factory.bind(GroupMember)
    dispatcher.filters_factory.bind(AuthorisedUser)
    dispatcher.filters_factory.bind(ChatWithABot)
