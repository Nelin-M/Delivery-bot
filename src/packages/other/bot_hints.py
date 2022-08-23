"""
The help menu in the bot
"""
from aiogram import types


async def bot_hints(dispatcher):
    """
    Implementation of hints for the user
    """
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
        ]
    )
