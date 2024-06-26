"""
Reaction to the cancel button
"""
from aiogram import types

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text="Назад")
async def cancel(message: types.Message):
    """
    Returns a response with a message to the user
    """
    await message.answer("Чтобы воспользоваться сервисом нажмите /start")
