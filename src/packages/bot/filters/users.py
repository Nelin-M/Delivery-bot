"""
Creating a filter
"""

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from src.packages.bot.loader import bot
from src.packages.loaders import env_variables
from src.packages.database import UserTable


class ChatWithABot(BoundFilter):
    """
    The filter allows you to carry out only personal correspondence with the bot
    """

    # pylint:disable=R0201,W0221
    async def check(self, message: types.Message):
        """
        Checks the chat type
        """

        return isinstance(message.chat.type, types.ChatType.PRIVATE)


class ChatWithABotCallback(BoundFilter):
    """
    The filter allows you to carry out only personal correspondence with the bot
    """

    # pylint:disable=R0201,W0221
    async def check(self, call: types.CallbackQuery):
        """
        Checks the chat type
        """

        return isinstance(call.message.chat.type, types.ChatType.PRIVATE)


class GroupMember(BoundFilter):
    """
    Checks whether the user is in a group
    """

    # pylint:disable=R0201,W0221
    async def check(self, message: types.Message):
        """
        Checks the status of the user in the group
        """
        chat_member = await bot.get_chat_member(chat_id=env_variables.get("CHANNEL_ID"), user_id=message.from_user.id)
        return chat_member.is_chat_member()


class GroupMemberCallback(BoundFilter):
    """
    Checks whether the user is in a group
    """

    # pylint:disable=R0201,W0221
    async def check(self, call: types.CallbackQuery):
        """
        Checks the status of the user in the group
        """
        chat_member = await bot.get_chat_member(
            chat_id=env_variables.get("CHANNEL_ID"), user_id=call.message.from_user.id
        )
        return chat_member.is_chat_member()


class AuthorisedUser(BoundFilter):
    """
    Checks if user authorised
    """

    # pylint:disable=R0201,W0221,W0511
    async def check(self, message: types.Message):  # TODO: Проверка осуществляется двумя запросами к БД, упростить
        """
        Overwritten checker
        @param message:
        @return:
        """
        user = await UserTable.get_by_telegram_id(message.from_user.id)
        return bool(user)
