"""
Setting up commands for feedback
"""
from aiogram import types

from src.packages.bot.filters import ChatWithABotCallback, GroupMemberCallback
from src.packages.bot.loader import dispatcher

from src.packages.bot.loader import bot
from src.packages.loaders import env_variables


@dispatcher.callback_query_handler(
    ChatWithABotCallback(), GroupMemberCallback(), lambda call: "Проверить подписку" in call.data
)
async def user_subscribe(call: types.CallbackQuery):
    """
    Reaction to the text /Проверить подписку
    """
    chat_member = await bot.get_chat_member(
        chat_id=env_variables.get("CHANNEL_ID"), user_id=int(call.data.split("|")[1])
    )
    if not chat_member.is_chat_member():
        await call.answer(
            "К сожалению администратор ещё не рассмотрел вашу заявку, пожалуйста, ожидайте. "
            "Обычно рассмотрение не занимает длительное время, возможно, в вашем случае понадобилась "
            "дополнительная проверка.",
            show_alert=True,
        )
    else:
        await call.message.answer(
            "Поздравляем, ваша заявка одобрена. Теперь можете смело нажать кнопку /menu и начать пользоваться ботом!"
        )
