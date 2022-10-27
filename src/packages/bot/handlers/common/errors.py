"""
This file processes messages that are not included in the main functionality
"""
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.packages.bot.filters import ChatWithABot, GroupMember
from src.packages.bot.loader import dispatcher
from src.packages.loaders import env_variables


@dispatcher.message_handler(ChatWithABot(), ~GroupMember())
async def not_signed(message: types.Message):
    """
    The function gives a button with a link to the group if the bot user is not subscribed to it
    """

    group_link = env_variables.get("CHANNEL_LINK")

    subscribe = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться", url=group_link),
                InlineKeyboardButton(
                    text="Проверить подписку", callback_data=f"Проверить подписку|{message.from_user.id}"
                ),
            ]
        ],
    )
    await message.answer(
        f"{message.from_user.first_name}, вы не подписаны на группу с заявками. Для использования бота, "
        f"вам необходимо отправить заявку на вступление в группу и дождаться пока администратор одобрит вашу заявку",
        reply_markup=subscribe,
    )


@dispatcher.message_handler(ChatWithABot(), GroupMember())
async def error(message: types.Message):
    """
    If you receive messages that are not processed
    """
    await message.answer("Я работаю только со встроенными командами")
