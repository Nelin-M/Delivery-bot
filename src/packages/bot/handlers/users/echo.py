"""
The file for implementing the echo bot
"""
from aiogram import types
from src.packages.bot.loader import dispatcher


@dispatcher.message_handler()
async def bot_echo(message: types.Message):
    """
    A function that returns user messages
    """
    await message.answer(message.text)
