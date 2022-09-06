"""
This file processes messages that are not included in the main functionality
"""
from aiogram import types

from src.packages.bot.filters import ChatWithABot, GroupMember
from src.packages.bot.keyboards.inline_buttons import subscribe
from src.packages.bot.loader import dispatcher


@dispatcher.message_handler(ChatWithABot(), ~GroupMember())
async def not_signed(message: types.Message):
    """
    The function gives a button with a link to the group if the bot user is not subscribed to it
    """
    await message.answer(f"{message.from_user.first_name} ты не подписан на группу", reply_markup=subscribe)


@dispatcher.message_handler(ChatWithABot(), GroupMember())
async def error(message: types.Message):
    """
    If you receive messages that are not processed
    """
    await message.answer("Я работаю только со встроенными командами")
