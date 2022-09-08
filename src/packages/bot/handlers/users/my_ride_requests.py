"""
This module handles users commands
"""
from aiogram import types
from aiogram.types import ParseMode, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import aiogram.utils.markdown as md

from src.packages.database import DatabaseException

# from src.packages.loaders import env_variables
from src.packages.bot.filters import GroupMember, ChatWithABot, AuthorisedUser
from src.packages.bot.loader import dispatcher, bot
from src.packages.database import database


def refactor_str(str_input):
    """
    This function refactor string
    @param str_input: str
    """
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0' + str_input}"


@dispatcher.message_handler(ChatWithABot(), GroupMember(), AuthorisedUser(), text=["Мои заявки"])
async def my_ride_requests_start(message: types.Message):
    """
    @param message: Message object
    """
    try:
        user = await database.select_user_by_tg_id(message.from_user.id)
        all_ride_requests = await database.select_all_requests_user(user.id)
        if all_ride_requests is None:
            bot.send_message(message.chat.id, "У вас нет созданных заявок.")
            return
        all_ride_requests.reverse()
        for ride_request in all_ride_requests:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(
                        # pylint: disable=line-too-long
                        f'{md.bold("Водитель: ")}{user.first_name} {user.last_name if user.last_name is not None else ""}'
                    ),
                    md.text(
                        f'{md.bold("Номер телефона: ")}'
                        f'{user.phone_number if user.phone_number is not None else "не указан"}'
                    ),
                    md.text(
                        f'{md.bold("Дата и время: ")}{refactor_str(ride_request.date.day)}.'
                        f"{refactor_str(ride_request.date.month)}.{ride_request.date.year} в "
                        f"{refactor_str(ride_request.time.hour)}:{refactor_str(ride_request.time.minute)}"
                    ),
                    md.text(
                        f"{md.bold('Условия довоза: ')}"
                        # pylint: disable=line-too-long
                        f"{ride_request.delivery_terms if ride_request.delivery_terms != 'Дальше' and ride_request.delivery_terms is not None else 'Не указано'}"
                    ),
                    md.text(
                        # pylint: disable=line-too-long
                        f'{md.bold("Место отправления: ")}{"" if ride_request.departure_place is None else ride_request.departure_place}'
                    ),
                    md.text(
                        # pylint: disable=line-too-long
                        f'{md.bold("Место прибытия: ")}{"" if ride_request.destination_place is None else ride_request.destination_place}'
                    ),
                    md.text(
                        # pylint: disable=line-too-long
                        f'{md.bold("Количество мест: ")}{"" if ride_request.seats_number is None else ride_request.seats_number}'
                    ),
                    sep="\n",
                ),
                parse_mode=ParseMode.MARKDOWN,
                # pylint: disable=W0511
                # TODO: переделать
                reply_markup=InlineKeyboardMarkup(
                    row_width=2,
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Удалить", callback_data=f"delete_ride_request|{ride_request.id}"
                            ),
                        ]
                    ],
                ),
            )
    except DatabaseException as error:
        await message.answer(text=str(error))


@dispatcher.callback_query_handler(lambda call: "delete_ride_request" in call.data)
async def send_message(call: CallbackQuery):
    """
    Handler for the delete button. `call.data` is passed the id of the ride request to be deleted
    :param call: CallbackQuery object
    """
    # ride_request_id = call.data.split('|')[1]
    # RideRequestTable.delete(ride_request_id)
    # channel_id = env_variables.get("GROUP_ID")
    # ride_request = RideRequestTable.get_by_id(ride_request_id)
    # bot.delete_message(channel_id, ride_request.tg_message_id)
    await call.answer("Заявка успешно удалена.", show_alert=True)
