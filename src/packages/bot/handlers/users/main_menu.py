"""
This module represents user enter menu depending on his membership in delivery group
"""
from aiogram import types
from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.keyboards import buttons
from .texts import MAIN_MENU_AUTHORISED


@dispatcher.message_handler(ChatWithABot(), GroupMember(), commands=["menu"])
async def authorised_user(message: types.Message):
    """
    This function greets authorised user
    @param message: Message object
    """
    await bot.send_message(
        message.chat.id,
        MAIN_MENU_AUTHORISED,
        reply_markup=buttons.main_menu_authorised,
        parse_mode=types.ParseMode.MARKDOWN,
    )
