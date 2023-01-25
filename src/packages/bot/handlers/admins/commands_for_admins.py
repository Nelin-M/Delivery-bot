"""
Commands for admin
"""
# pylint:disable=broad-except
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher
from src.packages.bot.other.throttling import rate_limit
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers

admins = env_variables.get("ADMINS_ID").replace(" ", "").split(",")


# Handler is off
@rate_limit(limit=10)
@dispatcher.message_handler(False, ChatWithABot(), GroupMember(), CommandStart(), user_id=admins)
async def admin_start(message: types.Message):
    """
    The /start command for the administrator
    """
    try:
        await message.answer(
            f"Привет, {message.from_user.first_name}, " f"ты администратор! " "Чтобы начать работу нажми /menu."
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: admin_start")
