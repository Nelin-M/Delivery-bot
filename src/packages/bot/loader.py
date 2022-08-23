"""
Loads variables for the handler
"""
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.packages.loaders import env_variables

bot = Bot(token=env_variables.get("API_KEY_TELEGRAM"), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
