"""
Creating a filter
"""

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from src.packages.bot.loader import bot
from src.packages.loaders import env_variables


class GroupMember(BoundFilter):
    """
    Checks whether the user is in a group
    """

    async def check(self, message: types.Message):
        """
        Checks the status of the user in the group
        """
        chat_member = await bot.get_chat_member(chat_id=env_variables.get("GROUP_ID"), user_id=message.from_user.id)
        return chat_member.status != "left"


class NotGroupMember(BoundFilter):
    """
    Checks not whether the user is in a group
    """

    async def check(self, message: types.Message):
        """
        Checks the status of the user in the group
        """
        chat_member = await bot.get_chat_member(chat_id=env_variables.get("GROUP_ID"), user_id=message.from_user.id)
        return chat_member.status == "left"
