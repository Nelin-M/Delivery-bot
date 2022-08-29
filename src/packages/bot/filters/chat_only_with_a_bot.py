"""
Creating a filter
"""

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ChatWithABot(BoundFilter):
    """
    The filter allows you to carry out only personal correspondence with the bot
    """

    async def check(self, message: types.Message):
        """
        Checks the chat type
        """

        return message.chat.type == types.ChatType.PRIVATE
