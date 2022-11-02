"""
Setting up commands for complaint
"""
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateComplaint
from src.packages.loaders import env_variables


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text="Пожаловаться")
async def write_complaint(message: types.Message):
    """
    Reaction to the text in inline button "Пожаловаться" and running the state machine
    """
    await message.answer(
        "Если сотрудник, повёл себя оскорбительно или у вас возник конфликт, опишите, пожалуйста, ситуацию."
        " Информация будет рассмотрена нашими модераторами и мы примем меры, при описание, укажите: номер машины"
        " или телеграм ник водителя или пассажира",
        reply_markup=buttons.car_edit_cancel,
    )
    await CreateComplaint.complaint_text.set()


@dispatcher.message_handler(state=CreateComplaint.complaint_text)
async def send_complaint_in_group(message: types.Message, state: FSMContext):
    """
    Shutting down the state machine and sending a message to the complaint chat
    """
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
    )
    await state.finish()
