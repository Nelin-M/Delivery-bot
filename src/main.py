"""
This file is the main one, the bot is launched from it.
"""
from aiogram import Bot as Bot_aiogram
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from packages.bot.chat_bot import Bot
from packages.logger.logger import Log, Loggers
from packages.loaders import config
from packages.loaders import env_variables

__all__ = ["main"]

logger = Log()
logger.info(Loggers.APP.value, "Bot session started;")

chat_bot = Bot(logger)

bot_aiogram = Bot_aiogram(env_variables["API_KEY_TELEGRAM"])
dp = Dispatcher(bot_aiogram)


@dp.message_handler(commands=["start"])
async def handle_start(message):
    """
    This handler will be called when user sends `/start` command.
    """
    await bot_aiogram.send_message(message.from_user.id, config["start_phrase"])


@dp.message_handler(commands=["help"])
async def handle_help(message):
    """
    This handler will be called when user sends `/help` command.
    """
    await bot_aiogram.send_message(message.from_user.id, config["help_phrase"])


@dp.message_handler(content_types=["text"])
async def handle_text(message):
    """
    This handler will be called when the user sends any text.
    Based on the received question, and answer is generated and sent to the user.
    """
    message_text = message.text
    logger.info(Loggers.INCOMING.value, f'"{message_text}";')
    await bot_aiogram.send_message(message.from_user.id, message_text)


def main():
    """
    The main function that starts the application.
    """
    executor.start_polling(dp)


if __name__ == "__main__":
    main()

logger.info(Loggers.APP.value, "Bot session ended.")
