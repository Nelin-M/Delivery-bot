"""
Utility for informing admins
"""
from aiogram import Dispatcher
from src.packages.logger import logger, Loggers
from src.packages.loaders import env_variables


async def inform_admins(dispatcher: Dispatcher):
    """
    The function sends a message to each admin when the bot is launched
    """
    try:
        admins = env_variables.get("ADMINS_ID")
        if admins is None:
            return
        admins = admins.replace(" ", "").split(",")
        for admin in admins:
            await dispatcher.bot.send_message(admin, "Бот запущен и готов к работе")
    except Exception as ex:
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: inform_admins")
