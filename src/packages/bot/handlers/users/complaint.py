"""
Setting up commands for complaint
"""
# pylint:disable=broad-except
import inspect

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateComplaint
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text="Пожаловаться")
async def write_complaint(message: types.Message):
    """
    Reaction to the text in inline button "Пожаловаться" and running the state machine
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await message.answer(
            "Если сотрудник, повёл себя оскорбительно или у вас возник конфликт, опишите, пожалуйста, ситуацию."
            " Информация будет рассмотрена нашими модераторами и мы примем меры, при описании, укажите: номер машины"
            " или телеграм ник водителя или пассажира",
            reply_markup=buttons.car_edit_cancel,
        )
        await CreateComplaint.complaint_text.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: write_complaint")


@dispatcher.message_handler(state=CreateComplaint.complaint_text)
async def send_complaint_in_group(message: types.Message, state: FSMContext):
    """
    Shutting down the state machine and sending a message to the complaint chat
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Отмена":
            await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
            return await state.finish()
        group_parameters = await message.bot.get_chat(env_variables.get("CHANNEL_COMPLAINT_ID"))
        answer = f"{message.text}\n\n[{message.from_user.username}]({message.from_user.url})"
        await bot.send_message(env_variables.get("CHANNEL_COMPLAINT_ID"), answer, parse_mode=types.ParseMode.MARKDOWN)
        await message.answer(
            "Обработка жалобы займет некоторое время. "
            f"Она будет опубликована \nв канале [{group_parameters.title}]({group_parameters.invite_link})",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=buttons.main_menu_authorised,
        )
        await state.finish()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: send_complaint_in_group")
