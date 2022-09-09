"""
Inline keyboard for the feedback group
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.packages.loaders import env_variables

channel_feedback_link = env_variables.get("CHANNEL_FEEDBACK_LINK")

feedback_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Оставить отзыв", callback_data="Оставить отзыв"),
            InlineKeyboardButton(text="Посмотреть отзывы", url=channel_feedback_link),
        ]
    ],
)
