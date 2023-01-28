"""
This module for creating taxi ride request
"""
import inspect
from datetime import datetime
import aiogram.utils.markdown as md
import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from src.packages.bot.filters import GroupMember, ChatWithABot
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateTaxiRideRequest
from src.packages.database import UserTable, RideRequestTable
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers

channel_id = env_variables.get("CHANNEL_ID")
channel_link = env_variables.get("CHANNEL_LINK")
bot_link = env_variables.get("BOT_LINK")


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


def handler_date(str_date: str):
    """
    This function refactor str in date
    """
    date_obj = datetime.strptime(str_date, "%d.%m")
    date_obj = date_obj.date()
    date_obj = date_obj.replace(year=datetime.now().year)
    return date_obj


def handler_time(str_time: str):
    """
    This function refactor str in time
    """
    time_obj = datetime.strptime(str_time, "%H:%M")
    time_obj = time_obj.time()
    return time_obj


def validation_date(text: str):
    """
    This function validates the date entered by the user
    """
    try:
        datetime.strptime(text, "%d.%m")
        return True
    except ValueError:
        return False


def validation_time(text: str):
    """
    This function validates the time entered by the user
    """
    try:
        datetime.strptime(text, "%H:%M")
        return True
    except ValueError:
        return False


def validation_number_seats(text: str):
    """
    This function validates the number_seats entered by the user
    """
    try:
        text = int(text)
    except ValueError:
        return False
    return 0 < int(text) < 8


@dispatcher.message_handler(state="*", commands="Отмена")
@dispatcher.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    This function to exit to the main menu
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Вы в главном меню", reply_markup=buttons.main_menu_authorised)
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: cancel_handler(создание заявки на такси)")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), Text(equals=["Такси"], ignore_case=True))
async def choice_date(message: types.Message):
    """
    This function transition to the state create taxi ride request and choice ride data
    @param message: Message object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value,
            tg_user_id,
            name_func,
            message_from_user,
            "Старт создания заявки на такси",
        )
        await CreateTaxiRideRequest.date.set()
        await message.answer(
            "Выберите дату " + emoji.emojize(":calendar:") + "\nИли напишите дату в формате XX.XX",
            reply_markup=buttons.get_date_keyboard(),
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: choice_date(создание заявки на такси)")


@dispatcher.message_handler(state=CreateTaxiRideRequest.date)
async def process_date(message: types.Message, state: FSMContext):
    """
    This function save ride data
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор даты(создание заявки на такси)"
        )
        if validation_date(message.text):
            async with state.proxy() as data:
                data["date_ride"] = handler_date(message.text)
            await CreateTaxiRideRequest.next()
            await message.answer(
                "Выберите время из предложенных или укажите время в формате XX:XX.\nНапример 07:15",
                reply_markup=buttons.time_keyboard,
            )
        else:
            await message.reply("Вы указали дату в неверном формате!")
            logger.warning_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Пользователь указал дату в неверном формате(создание заявки на такси)",
            )
            await message.answer(
                "Выберите дату " + emoji.emojize(":calendar:") + "\nИли напишите дату в формате XX.XX",
                reply_markup=buttons.get_date_keyboard(),
            )
            await CreateTaxiRideRequest.date.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_date(создание заявки на такси)")


@dispatcher.message_handler(state=CreateTaxiRideRequest.time)
async def process_time(message: types.Message, state: FSMContext):
    """
    This function save ride time
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор времени(создание заявки на такси)"
        )
        if validation_time(message.text):
            async with state.proxy() as data:
                data["time_ride"] = handler_time(message.text)
            await CreateTaxiRideRequest.next()
            await message.answer(
                "Введите условие довоза",
                reply_markup=buttons.keyboard_terms_delivery_taxi,
            )
        else:
            await message.reply("Вы указали время в неверном формате!\n")
            logger.warning_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Пользователь указал время в неверном формате(создание заявки на такси)",
            )
            await message.answer(
                "Выберите время из предложенных или укажите время в формате XX:XX.\nНапример 07:15",
                reply_markup=buttons.time_keyboard,
            )
            await CreateTaxiRideRequest.time.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_time(создание заявки на такси)")


@dispatcher.message_handler(state=CreateTaxiRideRequest.delivery_terms)
async def process_terms_delivery(message: types.Message, state: FSMContext):
    """
    This function save delivery terms
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value,
            tg_user_id,
            name_func,
            message_from_user,
            "Выбор условий довоза(создание заявки на такси)",
        )
        async with state.proxy() as data:
            data["delivery_terms"] = message.text
        await CreateTaxiRideRequest.next()
        await message.answer(
            "Введите или выберите место отправления\nНапример: «Маркса 22»",
            reply_markup=buttons.keyboard_place_departure,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(
            Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_terms_delivery(создание заявки на такси)"
        )


@dispatcher.message_handler(state=CreateTaxiRideRequest.place_departure)
async def process_place_departure(message: types.Message, state: FSMContext):
    """
    This function save departure place
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value,
            tg_user_id,
            name_func,
            message_from_user,
            "Выбор места отправления(создание заявки на такси)",
        )
        async with state.proxy() as data:
            data["departure_place"] = message.text
        await CreateTaxiRideRequest.next()
        await message.answer("Введите место прибытия\nНапример: «Маркса 22»", reply_markup=buttons.default_keyboard)
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(
            Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_departure(создание заявки на такси)"
        )


@dispatcher.message_handler(state=CreateTaxiRideRequest.place_coming)
async def process_place_coming(message: types.Message, state: FSMContext):
    """
    This function save destination place
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value,
            tg_user_id,
            name_func,
            message_from_user,
            "Выбор места прибытия(создание заявки на такси)",
        )
        async with state.proxy() as data:
            data["destination_place"] = message.text
        await CreateTaxiRideRequest.next()
        await message.answer(
            "Выберите или введите вручную количество мест в такси (без учёта вас):",
            reply_markup=buttons.number_of_seats_keyboard,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_coming(создание заявки на такси)")


@dispatcher.message_handler(state=CreateTaxiRideRequest.number_of_seats)
async def process_number_of_seats(message: types.Message, state: FSMContext):
    """
    This function save seats number
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value,
            tg_user_id,
            name_func,
            message_from_user,
            "Выбор кол-во мест(создание заявки на такси)",
        )
        if validation_number_seats(message.text):
            async with state.proxy() as data:
                data["seats_number"] = int(message.text)
            await CreateTaxiRideRequest.next()
            await message.answer(
                "Подтвердите создание заявки  " + emoji.emojize(":check_mark_button:"), reply_markup=buttons.keyboard_ok
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Автор заявки: ")}{escape_md(message.from_user.first_name)} {escape_md(message.from_user.last_name) if message.from_user.last_name is not None else ""} '
                    ),
                    md.text(
                        f'{emoji.emojize(":calendar:")}{md.bold(" Дата и время: ")}{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'
                        f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.{data["date_ride"].year if data.get("date_ride") is not None else ""} в '
                        f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'
                    ),
                    md.text(
                        f"{md.bold('Условия довоза: ')}\n"
                        f"{escape_md(data['delivery_terms']) if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"
                    ),
                    md.text(
                        f'{md.bold("🅰 Место отправления:")}\n{escape_md(data["departure_place"]) if data.get("departure_place") is not None else ""}'
                    ),
                    md.text(
                        f'{md.bold("🅱 Место прибытия:")}\n{escape_md(data["destination_place"]) if data.get("destination_place") is not None else ""}'
                    ),
                    md.text(
                        f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}'
                    ),
                    sep="\n",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await message.reply("Вы указали количество мест в неверном формате!\n")
            logger.warning_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Пользователь указал кол-во мест в неверном формате(создание заявки на такси)",
            )
            await message.answer("Выберите количество мест:", reply_markup=buttons.number_of_seats_keyboard)
            await CreateTaxiRideRequest.number_of_seats.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(
            Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_number_of_seats(создание заявки на такси)"
        )


@dispatcher.message_handler(state=CreateTaxiRideRequest.author)
async def process_driver(message: types.Message, state: FSMContext):
    """
    This function save ride request
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Отправить":
            async with state.proxy() as data:
                user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
                data["author"] = user_from_db.id
            data = await state.get_data()

            await state.finish()
            logger.info_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                f"Заявка создана{data}(создание заявки на такси)",
            )
            post_in_channel = await bot.send_message(
                channel_id,
                md.text(
                    md.text(
                        f"{emoji.emojize(':oncoming_taxi:')} Поиск попутчиков в такси"
                        f"\n\n"
                        f"{'#' + escape_md('набор_в_такси')}"
                        f"\n"
                        f"{'#' + escape_md(message.from_user.first_name.replace(' ', '_'))}{escape_md('_' + message.from_user.last_name.replace(' ', '_')) if message.from_user.last_name is not None else ''}"
                        f"\n"
                        f"{'#' + escape_md('такси_дата_') + refactor_str(data['date_ride'].day if data.get('date_ride') is not None else '')}{escape_md('_')}"
                        f"{refactor_str(data['date_ride'].month if data.get('date_ride') is not None else '')}{escape_md('_')}{data['date_ride'].year if data.get('date_ride') is not None else ''}"
                        f"\n"
                        f"{'#' + escape_md('такси_время_') + refactor_str(data['time_ride'].hour if data.get('time_ride') is not None else '')}"
                        f"{escape_md('_')}{refactor_str(data['time_ride'].minute if data.get('time_ride') is not None else '')}"
                        f"\n"
                    ),
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Автор поездки: ")}[{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name is not None else ""}]({message.from_user.url})'
                    ),
                    md.text(
                        f'{emoji.emojize(":calendar:")}{md.bold(" Дата и время: ")}'
                        f'{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'
                        f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.'
                        f'{data["date_ride"].year if data.get("date_ride") is not None else ""} в '
                        f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:'
                        f'{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'
                    ),
                    md.text(
                        f"{md.bold('Условия довоза: ')}\n"
                        f"{escape_md(data['delivery_terms']) if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"
                    ),
                    md.text(
                        f"{md.bold('🅰 Место отправления:')}\n{escape_md(data['departure_place']) if data.get('departure_place') is not None else ''}"
                    ),
                    md.text(
                        f'{md.bold("🅱 Место прибытия: ")}\n{escape_md(data["destination_place"]) if data.get("destination_place") is not None else ""}'
                    ),
                    md.text(
                        f'{md.bold("Количество мест: ")}{escape_md(data["seats_number"]) if data.get("seats_number") is not None else ""}'
                    ),
                    f"\nОтправить свою заявку вы можете при помощи бота: {escape_md(bot_link)}",
                    sep="\n",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text("Заявка создана"),
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Автор заявки: ")}[{escape_md(message.from_user.first_name)} {escape_md(message.from_user.last_name) if message.from_user.last_name is not None else ""}]({message.from_user.url}) '
                    ),
                    md.text(
                        f'{emoji.emojize(":calendar:")}{md.bold(" Дата и время: ")}'
                        f'{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'
                        f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.'
                        f'{data["date_ride"].year if data.get("date_ride") is not None else ""} в '
                        f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:'
                        f'{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'
                    ),
                    md.text(
                        f"{md.bold('Условия довоза: ')}\n"
                        f"{escape_md(data['delivery_terms']) if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"
                    ),
                    md.text(
                        f"{md.bold('🅰 Место отправления:')}\n{escape_md(data['departure_place']) if data.get('departure_place') is not None else ''}"
                    ),
                    md.text(
                        f'{md.bold("🅱 Место прибытия: ")}\n{escape_md(data["destination_place"]) if data.get("destination_place") is not None else ""}'
                    ),
                    md.text(
                        f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}'
                    ),
                    sep="\n",
                ),
                reply_markup=buttons.main_menu_authorised,
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    f"Данную заявку вы сможете найти в нижнем меню -> «Мои заявки» и [в канале с заявками]({channel_link})\n"
                    f"\nТвои пассажиры отметятся в комментариях под заявкой"
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await RideRequestTable.add(post_message_id=post_in_channel.message_id, **data)

        elif message.text == "Редактировать":
            await state.reset_state()
            await CreateTaxiRideRequest.date.set()
            await message.answer(
                "Выберите дату " + emoji.emojize(":calendar:"), reply_markup=buttons.get_date_keyboard()
            )
        else:
            await state.finish()
            await message.answer("Вы в главном меню:", reply_markup=buttons.main_menu_authorised)
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_driver(создание заявки на такси)")
