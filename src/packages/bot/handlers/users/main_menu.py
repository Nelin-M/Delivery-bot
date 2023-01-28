"""
This module represents user enter menu depending on his membership in delivery group
"""
import inspect

from aiogram import types
from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.keyboards import buttons
from src.packages.logger import logger, Loggers
from .texts import MAIN_MENU_AUTHORISED


@dispatcher.message_handler(ChatWithABot(), GroupMember(), commands=["menu"])
async def authorised_user(message: types.Message):
    """
    This function greets authorised user
    @param message: Message object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await bot.send_message(
            message.chat.id,
            MAIN_MENU_AUTHORISED,
            reply_markup=buttons.main_menu_authorised,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: authorised_user")
