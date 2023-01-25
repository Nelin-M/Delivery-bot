"""
Creating a filter
"""
import inspect

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from src.packages.bot.loader import bot
from src.packages.loaders import env_variables
from src.packages.database import UserTable, CarTable, DatabaseException, TelegramProfileTable
from src.packages.logger import logger, Loggers


class ChatWithABot(BoundFilter):
    """
    The filter allows you to carry out only personal correspondence with the bot
    """

    async def check(self, message: types.Message):
        """
        Checks the chat type
        """

        return message.chat.type == types.ChatType.PRIVATE


class ChatWithABotCallback(BoundFilter):
    """
    The filter allows you to carry out only personal correspondence with the bot
    """

    async def check(self, call: types.CallbackQuery):
        """
        Checks the chat type
        """

        return call.message.chat.type == types.ChatType.PRIVATE


class GroupMember(BoundFilter):
    """
    Checks whether the user is in a group
    """

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

    async def check(self, call: types.CallbackQuery):
        """
        Checks the status of the user in the group
        """
        chat_member = await bot.get_chat_member(
            chat_id=env_variables.get("CHANNEL_ID"), user_id=call.message.from_user.id
        )
        return chat_member.is_chat_member()


class HasCar(BoundFilter):
    """
    Checks if user has car
    """

    async def check(self, message: types.Message):  # TODO: Проверка осуществляется двумя запросами к БД, упростить
        """
        Overwritten checker
        @param message:
        @return:
        """
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        try:
            user = await UserTable.get_by_telegram_id(message.from_user.id)
        except DatabaseException:
            user = await UserTable.add(tg_id=message.from_user.id, car_id=None)
            await TelegramProfileTable.add(
                tg_id=message.from_user.id, user_id=user.id, nickname=message.from_user.username
            )
            logger.error_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "(Использование фильтра HasCar для незарегистрированного пользователя )",
            )
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "Пользователь добавлен в базу"
            )

        car = await CarTable.get_by_user_id(user.id)
        return bool(car)
