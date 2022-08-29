"""
Commands for admin
"""
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher
from src.packages.bot.other.throttling import rate_limit
from src.packages.loaders import env_variables

admins = env_variables.get("ADMINS").split(",")


@rate_limit(limit=10)
@dispatcher.message_handler(ChatWithABot(), GroupMember(), CommandStart(), user_id=admins)
async def admin_start(message: types.Message):
    """
    The /start command for the administrator
    """
    await message.answer(
        f"Привет, {message.from_user.first_name}, ты администратор! " "Чтобы начать работу нажми /menu."
    )
