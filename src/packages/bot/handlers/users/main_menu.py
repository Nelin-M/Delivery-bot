"""
This module represents user enter menu depending on his membership in delivery group
"""
from aiogram import types
from src.packages.bot.filters import GroupMember, ChatWithABot, AuthorisedUser
from src.packages.bot.loader import dispatcher
from src.packages.bot.keyboards import buttons
from .texts import MAIN_MENU_AUTHORISED, MAIN_MENU_UNAUTHORISED


@dispatcher.message_handler(ChatWithABot(), GroupMember(), AuthorisedUser(), commands=["menu"])
async def authorised_user(message: types.Message):
    """
    This function greets authorised user
    @param message: Message object
    """
    await message.answer(text=MAIN_MENU_AUTHORISED, reply_markup=buttons.main_menu_authorised)


@dispatcher.message_handler(ChatWithABot(), GroupMember(), ~AuthorisedUser(), commands=["menu"])
async def unauthorised_user(message: types.Message):
    """
    This function greets unauthorised user
    @param message: Message object
    """
    await message.answer(text=MAIN_MENU_UNAUTHORISED, reply_markup=buttons.main_menu_unauthorised)
