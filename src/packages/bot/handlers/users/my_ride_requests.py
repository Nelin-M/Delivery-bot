"""
This module handles users commands
"""
import inspect

from aiogram import types
from aiogram.types import ParseMode, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import aiogram.utils.markdown as md

from src.packages.database import DatabaseException

from src.packages.loaders import env_variables
from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher, bot
from src.packages.database import UserTable, RideRequestTable
from src.packages.logger import logger, Loggers


def refactor_str(str_input):
    """
    This function refactor string
    @param str_input: str
    """
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0' + str_input}"


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text=["Мои заявки"])
async def my_ride_requests_start(message: types.Message):
    """
    @param message: Message object
    """
    tg_user_id = message.from_user.id
    message_from_user = message.text
    name_func = inspect.getframeinfo(inspect.currentframe()).function
    logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
    try:
        user = await UserTable.get_by_telegram_id(message.from_user.id)
        all_ride_requests = await RideRequestTable.get_user_ride_requests(user.id)
        if len(all_ride_requests) == 0:
            await bot.send_message(message.chat.id, "У вас нет созданных заявок.")
            return
        all_ride_requests.reverse()
        for ride_request in all_ride_requests:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(
                        f'{md.bold("Водитель: ")}'
                        f'{message.from_user.first_name if message.from_user.first_name is not None else ""} '
                        f'{message.from_user.last_name if message.from_user.last_name is not None else ""} '
                    ),
                    md.text(
                        f'{md.bold("Дата и время: ")}{refactor_str(ride_request.date.day)}.'
                        f"{refactor_str(ride_request.date.month)}.{ride_request.date.year} в "
                        f"{refactor_str(ride_request.time.hour)}:{refactor_str(ride_request.time.minute)}"
                    ),
                    md.text(
                        f"{md.bold('Условия довоза: ')}"
                        f"{ride_request.delivery_terms if ride_request.delivery_terms != 'Дальше' and ride_request.delivery_terms is not None else 'Не указано'}"  # pylint: disable=line-too-long
                    ),
                    md.text(
                        f'{md.bold("Место отправления: ")}{"" if ride_request.departure_place is None else ride_request.departure_place}'  # pylint: disable=line-too-long
                    ),
                    md.text(
                        f'{md.bold("Место прибытия: ")}{"" if ride_request.destination_place is None else ride_request.destination_place}'  # pylint: disable=line-too-long
                    ),
                    md.text(
                        f'{md.bold("Количество мест: ")}{"" if ride_request.seats_number is None else ride_request.seats_number}'  # pylint: disable=line-too-long
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
        logger.info_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Показ пользователю списка заявок"
        )
    except DatabaseException as error:
        logger.error_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, str(error))
        await message.answer(text=str(error))


@dispatcher.callback_query_handler(lambda call: "delete_ride_request" in call.data)
async def send_message(call: CallbackQuery):
    """
    Handler for the delete button. `call.data` is passed the id of the ride request to be deleted
    :param call: CallbackQuery object
    """

    tg_user_id = dict(call).get("from").get("id")
    message_from_user = dict(call).get("data")
    name_func = inspect.getframeinfo(inspect.currentframe()).function
    ride_request_id = int(call.data.split("|")[1])
    try:
        ride_request = await RideRequestTable.get_single_ride_request(ride_request_id)
    except DatabaseException:
        logger.warning_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Заявка не найдена в базе данных"
        )
    channel_id = env_variables.get("CHANNEL_ID")
    try:
        await bot.delete_message(channel_id, ride_request.post_message_id)
    except UnboundLocalError:
        logger.warning_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Удаление несуществующей заявки"
        )
    try:
        await RideRequestTable.delete(ride_request_id)
    except DatabaseException:
        logger.warning_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Заявка не найдена в базе данных"
        )
    await call.answer(
        "Заявка успешно удалена.\nДля просмотра обновленного списка заявок, вновь нажмите «Мои заявки»", show_alert=True
    )
    logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Заявка удалена")
