"""
Basic commands for the user
"""

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher


@dispatcher.message_handler(ChatWithABot(), GroupMember(), CommandStart())
async def user_start(message: types.Message):
    """
    Reaction to the /start command
    """
    await message.answer(
        f"Привет, {message.from_user.first_name}, ты пользователь группы Delivery_bot!"
        "Чтобы начать работу нажми /menu"
    )


@dispatcher.message_handler(ChatWithABot(), GroupMember(), CommandHelp())
async def user_help(message: types.Message):
    """
    Reaction to the /help command
    """
    await message.answer("Здесь можно прописать про использование бота")
