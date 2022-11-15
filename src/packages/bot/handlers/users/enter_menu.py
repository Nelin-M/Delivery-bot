"""
Basic commands for the user
"""
# pylint:disable=broad-except
import inspect

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher
from src.packages.database import TelegramProfileTable, UserTable, DatabaseException
from src.packages.logger import logger, Loggers


@dispatcher.message_handler(ChatWithABot(), GroupMember(), CommandStart())
async def user_start(message: types.Message):
    """
    Reaction to the /start command
    """
    try:
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
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "пользователь добавлен в базу"
            )
        await message.answer(
            "Поздравляем, ваша заявка одобрена. Теперь можете смело нажать кнопку /menu и начать пользоваться ботом!"
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: user_start")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), CommandHelp())
async def user_help(message: types.Message):
    """
    Reaction to the /help command
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await message.answer("Здесь можно прописать про использование бота")
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: user_help")
