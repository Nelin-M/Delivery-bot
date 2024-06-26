"""
Inline keyboard link to the group
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.packages.loaders import env_variables

channel_link = env_variables.get("CHANNEL_LINK")

subscribe = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписаться", url=channel_link),
            InlineKeyboardButton(text="Проверить подписку", callback_data="Проверить подписку"),
        ]
    ],
)
