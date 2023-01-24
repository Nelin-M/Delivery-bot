"""
Setting up commands for feedback
"""
# pylint:disable=broad-except
import inspect

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot, ChatWithABotCallback, GroupMemberCallback
from src.packages.bot.keyboards import inline_buttons, buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateReview
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text="Обратная связь")
async def user_start(message: types.Message):
    """
    Reaction to the text /Обратная связь
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await message.answer(
            "Вы можете посмотреть или оставить отзыв о работе нашего сервиса!",
            reply_markup=inline_buttons.feedback_keyboard,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: user_start(обратная связь)")


@dispatcher.callback_query_handler(ChatWithABotCallback(), GroupMemberCallback(), text="Оставить отзыв")
async def write_review(call: types.CallbackQuery):
    """
    Reaction to the text in inline button "Оставить отзыв" and running the state machine
    """
    try:
        tg_user_id = dict(call).get("from").get("id")
        message_from_user = dict(call).get("data")
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await call.message.answer(
            "Ваш отзыв будет опубликован в группе, ждем предложений и пожеланий:", reply_markup=buttons.car_edit_cancel
        )
        await CreateReview.review_text.set()
    except Exception as ex:
        await call.message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: write_review(обратная связь)")


@dispatcher.message_handler(state=CreateReview.review_text)
async def send_review_in_group(message: types.Message, state: FSMContext):
    """
    Shutting down the state machine and sending a message to the feedback chat
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Отмена":
            await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
            return await state.finish()
        group_parameters = await message.bot.get_chat(env_variables.get("CHANNEL_FEEDBACK_ID"))
        answer = f"{message.text}\n\n[{message.from_user.username}]({message.from_user.url})"
        await bot.send_message(env_variables.get("CHANNEL_FEEDBACK_ID"), answer, parse_mode=types.ParseMode.MARKDOWN)
        await message.answer(
            "Спасибо, что оставили, отзыв о нашем сервисе, мы постараемся учесть все замечания и "
            "обязательно их добавить в следующем обновлении, чтобы стать ещё удобнее для вас!\n\n"
            f"Ваш отзыв будет опубликован \nв канале [{group_parameters.title}]({group_parameters.invite_link})",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=buttons.main_menu_authorised,
        )

        await state.finish()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: send_review_in_group(обратная связь)")
