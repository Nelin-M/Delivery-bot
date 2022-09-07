"""
Utility for informing admins
"""

from aiogram import Dispatcher
from src.packages.logger import logger, Loggers
from src.packages.loaders import env_variables

admins = env_variables.get("ADMINS").split(",")


async def inform_admins(dispatcher: Dispatcher):
    """
    The function sends a message to each admin when the bot is launched
    """
    for admin in admins:
        try:
            await dispatcher.bot.send_message(admin, "Бот Запущен и готов к работе")
        # pylint: disable=broad-except
        except Exception as exception:
            logger.critical(Loggers.APP.value, f"Unexpected error: {exception}")
