"""
Initializing modules
"""

from aiogram import Dispatcher
from .only_for_group_members import GroupMember, NotGroupMember
from .chat_only_with_a_bot import ChatWithABot


def setup_filters(dispatcher: Dispatcher):
    """
    Registration of filters
    """

    dispatcher.filters_factory.bind(GroupMember)
    dispatcher.filters_factory.bind(NotGroupMember)
    dispatcher.filters_factory.bind(ChatWithABot)
