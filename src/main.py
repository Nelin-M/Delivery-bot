"""
This file is the main one, the bot is launched from it.
"""
from aiogram import executor

from src.packages.database import database, setup_database
from src.packages.bot.handlers import dispatcher
from src.packages.bot.other.bot_hints import bot_hints
from src.packages.bot.other.inform_admins import inform_admins
from src.packages.logger import logger, Loggers
from src.packages.bot.middlewares import setup_middleware
from src.packages.bot.filters import setup_filters

logger.info(Loggers.APP.value, "Bot session started;")


async def connecting_file(load_dispatcher):
    """
    The function adds additional functionality
    """

    await setup_database(database)  # TODO: Не совсем понятен момент с инициализацией БД

    setup_filters(dispatcher)
    setup_middleware(dispatcher)

    await bot_hints(load_dispatcher)
    await inform_admins(load_dispatcher)


def main():
    """
    The main function that starts the application.
    """
    executor.start_polling(dispatcher, on_startup=connecting_file)


if __name__ == "__main__":
    main()

logger.info(Loggers.APP.value, "Bot session ended.")
