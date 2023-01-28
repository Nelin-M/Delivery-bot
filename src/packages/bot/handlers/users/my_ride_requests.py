"""
This module handles users commands
"""
# pylint:disable=broad-except
import inspect
from aiogram import types
from aiogram.types import ParseMode, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import aiogram.utils.markdown as md
from aiogram.utils.exceptions import MessageCantBeDeleted
from src.packages.bot.keyboards import buttons
from src.packages.database import DatabaseException
from src.packages.loaders import env_variables
from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.loader import dispatcher, bot
from src.packages.database import UserTable, RideRequestTable
from src.packages.logger import logger, Loggers


def escape_md(text: str or int):
    # todo: найти аналог в библиотеке
    text = str(text)
    text = text.replace("_", "\\_")
    text = text.replace("*", "\\*")
    text = text.replace("`", "\\`")
    text = text.replace("~", "\\~")
    text = text.replace("|", "\\|")
    return text


def refactor_str(str_input: str or int):
    """
    This function refactor string
    """
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0' + str_input}"


def get_inline_delete_button(ride_request_id: int):
    return (
        InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Удалить", callback_data=f"delete_ride_request|{ride_request_id}"),
                ]
            ],
        ),
    )


page = 0
all_ride_requests = []


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text=["Мои заявки"])
async def my_ride_requests_start(message: types.Message):
    """
    @param message: Message object
    """
    try:
        global page
        global all_ride_requests
        page = 0
        all_ride_requests = []
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
            await show_requests(message)
            logger.info_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Показ пользователю списка заявок"
            )
        except DatabaseException as error:
            logger.error_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, str(error))
            await message.answer(text=str(error))
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: my_ride_requests_start")


async def show_requests(message: types.Message):
    for i in range(5 * page, min(5 * (page + 1), len(all_ride_requests))):
        ride_request = all_ride_requests[i]
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(
                    f'{md.bold("Дата и время: ")}{refactor_str(ride_request.date.day)}.'
                    f"{refactor_str(ride_request.date.month)}.{ride_request.date.year} в "
                    f"{refactor_str(ride_request.time.hour)}:{refactor_str(ride_request.time.minute)}"
                ),
                md.text(
                    f"{md.bold('Условия довоза: ')}"
                    f"{escape_md(ride_request.delivery_terms) if ride_request.delivery_terms != 'Дальше' and ride_request.delivery_terms is not None else 'Не указано'}"
                ),
                md.text(
                    f'{md.bold("Место отправления: ")}{"" if ride_request.departure_place is None else escape_md(ride_request.departure_place)}'
                ),
                md.text(
                    f'{md.bold("Место прибытия: ")}{"" if ride_request.destination_place is None else escape_md(ride_request.destination_place)}'
                ),
                md.text(
                    f'{md.bold("Количество мест: ")}{"" if ride_request.seats_number is None else ride_request.seats_number}'
                ),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                row_width=2,
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Удалить", callback_data=f"delete_ride_request|{ride_request.id}"),
                    ]
                ],
            ),
        )
    if len(all_ride_requests) > 5 * (page + 1):
        await bot.send_message(
            message.chat.id,
            "Вывести следующие заявки?",
            reply_markup=InlineKeyboardMarkup(
                row_width=2,
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да", callback_data="more_requests"),
                    ]
                ],
            ),
        )


@dispatcher.callback_query_handler(lambda c: c.data == "more_requests")
async def process_callback_more_requests(callback_query: types.CallbackQuery):
    global page
    page += 1
    await show_requests(callback_query.message)


@dispatcher.callback_query_handler(lambda call: "delete_ride_request" in call.data)
async def send_message(call: CallbackQuery):
    """
    Handler for the delete button. `call.data` is passed the id of the ride request to be deleted
    :param call: CallbackQuery object
    """
    try:
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
        # todo: точно такое исключение должно быть?
        except UnboundLocalError as e:
            logger.warning_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, f"Удаление несуществующей заявки {e}"
            )
        except MessageCantBeDeleted as e:
            logger.info_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                f"Сообщение с заявкой не получается удалить {e}",
            )
            await call.answer(
                "С момента публикации вашей заявки прошло 48 часов, для удаления вам понадобится помощь администратора",
                show_alert=True,
            )
            return
        try:
            await RideRequestTable.delete(ride_request_id)
        except DatabaseException:
            logger.warning_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Заявка не найдена в базе данных"
            )
        await call.answer(
            "Заявка успешно удалена.\nДля просмотра обновленного списка заявок, вновь нажмите «Мои заявки»",
            show_alert=True,
        )
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Заявка удалена")
    except Exception as ex:
        await call.answer("По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже")
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: send_message(удаление авто)")
