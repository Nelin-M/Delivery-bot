"""
Setting up commands for feedback
"""
# pylint:disable=broad-except
import inspect

from aiogram import types

from src.packages.bot.filters import ChatWithABotCallback, GroupMemberCallback
from src.packages.bot.loader import dispatcher

from src.packages.bot.loader import bot
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers


@dispatcher.callback_query_handler(
    ChatWithABotCallback(), GroupMemberCallback(), lambda call: "Проверить подписку" in call.data
)
async def user_subscribe(call: types.CallbackQuery):
    """
    Reaction to the text /Проверить подписку
    """
    try:
        tg_user_id = dict(call).get("from").get("id")
        message_from_user = dict(call).get("data")
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        chat_member = await bot.get_chat_member(
            chat_id=env_variables.get("CHANNEL_ID"), user_id=int(call.data.split("|")[1])
        )
        if not chat_member.is_chat_member():
            await call.answer(
                "Администратор ещё не одобрил вашу заявку. Возможно, понадобилась дополнительная проверка❗Чтобы узнать "
                "статус заявки, нажмите кнопку «Проверить подписку» немного позже",
                show_alert=True,
            )
            logger.info_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Заявка пользователя на вступление в группу не рассмотрена",
            )
        else:
            await call.message.answer(
                "Поздравляем, ваша заявка одобрена. "
                "Теперь можете смело нажать кнопку /menu и начать пользоваться ботом!"
            )
            logger.info_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Заявка пользователя на вступление в группу рассмотрена",
            )
    except Exception as ex:
        await call.answer("По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже")
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: user_subscribe")
