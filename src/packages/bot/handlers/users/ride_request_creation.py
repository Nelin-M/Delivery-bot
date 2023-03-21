"""
This module for creating ride request
"""
import inspect
import re
from datetime import datetime, timedelta
import aiogram.utils.markdown as md
import emoji
from geopy import Yandex
from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.packages.bot.filters import GroupMember, ChatWithABot, HasCar
from src.packages.bot.keyboards import buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateRideRequest
from src.packages.database import UserTable, RideRequestTable, CarTable
from src.packages.loaders import env_variables
from src.packages.logger import logger, Loggers

channel_id = env_variables.get("CHANNEL_ID")
channel_link = env_variables.get("CHANNEL_LINK")
bot_link = env_variables.get("BOT_LINK")
api_key_yandex_geokoder = env_variables.get("API_KEY_YANDEX_GEOKODER")
route_type = "auto"


def remove_characters_for_create_hashtag(text: str):
    return re.sub(r"[^a-zA-Zа-яА-я0-9_]", "", text)


def escape_md(text: str or int):
    # todo: найти аналог в библиотеке aiogram
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


def validate_date_three(date_obj):
    """
    This function date validation so that the date is less than 3 days old
    """
    return date_obj <= datetime.now().date() + timedelta(days=2)


def create_link_maps(address_1: str, address_2: str):
    """The function generates a route link for two addresses"""
    try:
        geolocator = Yandex(api_key=api_key_yandex_geokoder)
        location_1 = geolocator.geocode("Омск " + address_1)
        location_2 = geolocator.geocode("Омск " + address_2)
        return f"https://yandex.ru/maps/?rtext={location_1.latitude},{location_1.longitude}~{location_2.latitude},{location_2.longitude}&rtt={route_type}"
    except GeocoderTimedOut:
        logger.info(
            Loggers.INCOMING.value,
            "Cервер API яндекс карт недоступен",
        )
        raise GeocoderTimedOut
    except AttributeError:
        logger.info(
            Loggers.INCOMING.value,
            "Пользователь неверно ввел адрес",
        )
        raise AttributeError
    except GeocoderInsufficientPrivileges:
        logger.warning(
            Loggers.INCOMING.value,
            "Неверный API/нет доступа к API/403 Forbiden",
        )
        raise GeocoderInsufficientPrivileges


@dispatcher.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
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
        if current_state is not None:
            await state.finish()
        await message.answer("Вы в главном меню", reply_markup=buttons.main_menu_authorised)
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: cancel_handler(создание заявки)")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), Text(equals=["Создать заявку"], ignore_case=True))
async def choice_date(message: types.Message):
    """
    This function transition to the state create ride request and choice ride data
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
            "Старт создания заявки(у пользователя есть авто)",
        )
        await CreateRideRequest.date.set()

        await message.answer(
            "Выберите дату " + emoji.emojize(":calendar:") + "\nИли напишите дату в формате XX.XX",
            reply_markup=buttons.get_date_keyboard(),
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: choice_date(создание заявки)")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), ~HasCar(), Text(equals=["Создать заявку"], ignore_case=True))
async def not_car(message: types.Message):
    """
    This function shows message use without car
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
            "Старт создания заявки(у пользователя нет авто)",
        )
        await message.answer(
            "Для создания заявки необходимо добавить машину в разделе \n«Мой автомобиль»\n\nНажмите на кнопку ниже",
            reply_markup=buttons.keyboard_main_profile,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: not_car(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.date)
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
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор даты")
        if validation_date(message.text) and validate_date_three(handler_date(message.text)):
            async with state.proxy() as data:
                data["date_ride"] = handler_date(message.text)
            await CreateRideRequest.next()
            await message.answer(
                "Выберите время из предложенных или укажите время в формате XX:XX.\nНапример 07:15",
                reply_markup=buttons.time_keyboard,
            )
        else:
            await message.reply("Максимальная дата заявки 3 дня вместе с текущим, выберите дату из предложенных")
            logger.info_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Пользователь указал дату в неверном формате",
            )
            await message.answer(
                "Выберите дату " + emoji.emojize(":calendar:") + "\nИли напишите дату в формате XX.XX",
                reply_markup=buttons.get_date_keyboard(),
            )
            await CreateRideRequest.date.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_date(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.time)
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
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор времени")
        if validation_time(message.text):
            async with state.proxy() as data:
                data["time_ride"] = handler_time(message.text)
            await CreateRideRequest.next()
            await message.answer(
                "Введите условие довоза\nНапример: «за шоколадку»\nИли нажмите «дальше»"
                "\nОбратите внимание, любые виды денежной компенсации указывать запрещено",
                reply_markup=buttons.keyboard_terms_delivery,
            )
        else:
            await message.reply("Вы указали время в неверном формате!\n")
            logger.warning_from_handlers(
                Loggers.INCOMING.value,
                tg_user_id,
                name_func,
                message_from_user,
                "Пользователь указал время в неверном формате",
            )
            await message.answer(
                "Выберите время из предложенных или укажите время в формате XX:XX.\nНапример 07:15",
                reply_markup=buttons.time_keyboard,
            )
            await CreateRideRequest.time.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_time(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.delivery_terms)
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
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор условий довоза"
        )
        if message.text == "Не прикреплять ссылку":
            await message.answer(
                "Выберите или введите вручную комфортное количество мест (без учёта вас):",
                reply_markup=buttons.number_of_seats_keyboard,
            )
            await CreateRideRequest.number_of_seats.set()
        elif message.text == "Да":
            await CreateRideRequest.next()
            user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
            text = await RideRequestTable.get_user_ride_request_last_departure_place(user_from_db.id)
            await message.answer(
                "Введите место отправления в формате: «Улица, номер дома» или выберите из предложенного:",
                reply_markup=buttons.create_dinamic_keyboard(text),
            )
        else:
            async with state.proxy() as data:
                data["delivery_terms"] = message.text
            await CreateRideRequest.next()
            user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
            text = await RideRequestTable.get_user_ride_request_last_departure_place(user_from_db.id)
            await message.answer(
                "Введите место отправления в формате: «Улица, номер дома» или выберите из предложенного:",
                reply_markup=buttons.create_dinamic_keyboard(text),
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_terms_delivery(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.place_departure)
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
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор места отправления"
        )

        async with state.proxy() as data:
            data["departure_place"] = message.text
        await CreateRideRequest.next()
        user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
        text = await RideRequestTable.get_user_ride_request_last_destination_place(user_from_db.id)
        await message.answer(
            "Введите место прибытия в формате: «Улица, номер дома»",
            reply_markup=buttons.create_dinamic_default_keyboard(text),
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_departure(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.place_coming)
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
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор места прибытия"
        )

        async with state.proxy() as data:
            data["destination_place"] = message.text
        async with state.proxy() as data:
            try:
                route_link = create_link_maps(data["departure_place"], data["destination_place"])
                data["route_link"] = route_link
                await CreateRideRequest.next()
                await message.answer(
                    f"Перейдите по [ссылке]({route_link}) и проверьте, совпадает ли ваш маршрут с предложенным. Если совпадает, то нажмите да, ссылка будет прикреплена к заявке",
                    reply_markup=buttons.yes_no_keyboard,
                    parse_mode=ParseMode.MARKDOWN,
                )
                await CreateRideRequest.route_link.set()
            except (GeocoderTimedOut, GeocoderInsufficientPrivileges):
                await message.answer(
                    "Выберите или введите вручную комфортное количество мест (без учёта вас):",
                    reply_markup=buttons.number_of_seats_keyboard,
                )
                await CreateRideRequest.number_of_seats.set()
            except AttributeError:
                await message.answer(
                    "Неверно введено место отправления или место прибытия\nХотите снова ввести данные?",
                    reply_markup=buttons.yes_no_keyboard,
                )
                await CreateRideRequest.delivery_terms.set()

    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_coming(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.place_departure_update)
async def place_departure_update(message: types.Message, state: FSMContext):
    """
    This function update departure place and transition in state route_link
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Исправление места отправления"
        )

        async with state.proxy() as data:
            data["departure_place"] = message.text
        async with state.proxy() as data:
            try:
                route_link = create_link_maps(data["departure_place"], data["destination_place"])
                data["route_link"] = route_link
                await CreateRideRequest.next()
                await message.answer(
                    f"Перейдите по [ссылке]({route_link}) и проверьте, совпадает ли ваш маршрут с предложенным. Если совпадает, то нажмите да, ссылка будет прикреплена к заявке",
                    reply_markup=buttons.yes_no_keyboard,
                    parse_mode=ParseMode.MARKDOWN,
                )
                await CreateRideRequest.route_link.set()
            except (GeocoderTimedOut, GeocoderInsufficientPrivileges):
                await message.answer(
                    "Выберите или введите вручную комфортное количество мест (без учёта вас):",
                    reply_markup=buttons.number_of_seats_keyboard,
                )
                await CreateRideRequest.number_of_seats.set()
            except AttributeError:
                await message.answer(
                    "Неверно введено место отправления или место прибытия\nХотите снова ввести данные?",
                    reply_markup=buttons.yes_no_keyboard,
                )
                await CreateRideRequest.delivery_terms.set()

    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_coming(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.route_link)
async def process_route_link(message: types.Message, state: FSMContext):
    """
    This function save route link
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Ссылка на маршрут")
        if message.text == "Изменить место отправления":
            async with state.proxy() as data:
                if data.get("route_link") is not None:
                    del data["route_link"]
            user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
            text = await RideRequestTable.get_user_ride_request_last_departure_place(user_from_db.id)
            await message.answer(
                "Введите место отправления в формате: «Улица, номер дома» или выберите из предложенного:",
                reply_markup=buttons.create_dinamic_keyboard(text),
            )
            await CreateRideRequest.place_departure_update.set()
        elif message.text == "Изменить место прибытия":
            async with state.proxy() as data:
                if data.get("route_link") is not None:
                    del data["route_link"]
            user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
            text = await RideRequestTable.get_user_ride_request_last_destination_place(user_from_db.id)
            await message.answer(
                "Введите место прибытия в формате: «Улица, номер дома»",
                reply_markup=buttons.create_dinamic_default_keyboard(text),
            )
            await CreateRideRequest.place_coming.set()
        else:
            async with state.proxy() as data:
                data["route_link"] = data["route_link"] if message.text == "Да" else ""
                logger.info_from_handlers(
                    Loggers.INCOMING.value,
                    tg_user_id,
                    name_func,
                    message_from_user,
                    f"Ссылка на маршрут {data['route_link']} {'' if message.text == 'Да' else 'не'} добавлена к заявке",
                )
            await CreateRideRequest.next()
            await message.answer(
                "Выберите или введите вручную комфортное количество мест (без учёта вас):",
                reply_markup=buttons.number_of_seats_keyboard,
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_place_coming(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.number_of_seats)
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
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "Выбор кол-во мест")
        if validation_number_seats(message.text):
            async with state.proxy() as data:
                data["seats_number"] = int(message.text)
                user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
                car = await CarTable.get_by_user_id(user_from_db.id)
            await CreateRideRequest.next()
            await message.answer(
                "Подтвердите создание заявки  " + emoji.emojize(":check_mark_button:"), reply_markup=buttons.keyboard_ok
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Водитель: ")}{escape_md(message.from_user.first_name)} {escape_md(message.from_user.last_name) if message.from_user.last_name is not None else ""} '
                    ),
                    md.text(
                        f'{emoji.emojize(":oncoming_automobile:")}{md.bold(" Машина: ")}'
                        f"{escape_md(car.brand)} {escape_md(car.model)} ({car.number_plate[:6]} {car.number_plate[6:]})"
                    ),
                    md.text(
                        f'{emoji.emojize(":calendar:")}{md.bold(" Дата и время: ")}{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'
                        f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.{refactor_str(data["date_ride"].year) if data.get("date_ride") is not None else ""} в '
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
                        f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}\n'
                    ),
                    md.text(
                        f'🚩Для уточнения маршрута перейдите по [ссылке]({data["route_link"]})'
                        if data.get("route_link") is not None
                        and data.get("route_link")
                        and len(data.get("route_link")) > 0
                        else ""
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
                "Пользователь указал кол-во мест в неверном формате",
            )
            await message.answer("Выберите количество мест:", reply_markup=buttons.number_of_seats_keyboard)
            await CreateRideRequest.number_of_seats.set()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_number_of_seats(создание заявки)")


@dispatcher.message_handler(state=CreateRideRequest.driver)
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
            car = await CarTable.get_by_user_id(user_from_db.id)
            await state.finish()
            logger.info_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, f"Заявка создана{data}"
            )
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text("Заявка создана"),
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Водитель: ")}[{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name is not None else ""}]({message.from_user.url}) '
                    ),
                    md.text(
                        f'{emoji.emojize(":oncoming_automobile:")}{md.bold(" Машина: ")}'
                        f"{escape_md(car.brand)} {escape_md(car.model)} ({car.number_plate[:6]} {car.number_plate[6:]})"
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
                        f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}\n'
                    ),
                    md.text(
                        f'🚩Для уточнения маршрута перейдите по [ссылке]({data["route_link"]})'
                        if data.get("route_link") is not None
                        and data.get("route_link")
                        and len(data.get("route_link")) > 0
                        else ""
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
            processed_name = (
                message.from_user.first_name
                if message.from_user.last_name is None
                else message.from_user.first_name + "_" + message.from_user.last_name
            )
            processed_name = processed_name.replace(" ", "_")
            processed_name = remove_characters_for_create_hashtag(processed_name)
            if processed_name == "":
                processed_name = "id_" + str(message.from_user.id % 10000)
            processed_name = escape_md(processed_name)
            post_in_channel = await bot.send_message(
                channel_id,
                md.text(
                    md.text(
                        f"{emoji.emojize(':wheel:')} Заявка от водителя"
                        f"\n\n"
                        f"{'#' + escape_md('водитель')}"
                        f"\n"
                        f"{'#' + processed_name}"
                        f"\n"
                        f"{'#' + escape_md('водитель_дата_') + refactor_str(data['date_ride'].day if data.get('date_ride') is not None else '')}{escape_md('_')}"
                        f"{refactor_str(data['date_ride'].month if data.get('date_ride') is not None else '')}{escape_md('_')}{data['date_ride'].year if data.get('date_ride') is not None else ''}"
                        f"\n"
                        f"{'#' + escape_md('водитель_время_') + refactor_str(data['time_ride'].hour if data.get('time_ride') is not None else '')}"
                        f"{escape_md('_')}{refactor_str(data['time_ride'].minute if data.get('time_ride') is not None else '')}"
                        f"\n"
                    ),
                    md.text(
                        f'{emoji.emojize(":bust_in_silhouette:")}{md.bold(" Водитель: ")}[{escape_md(message.from_user.first_name)} {escape_md(message.from_user.last_name) if message.from_user.last_name is not None else ""}]({message.from_user.url}) '
                    ),
                    md.text(
                        f'{emoji.emojize(":oncoming_automobile:")}{md.bold(" Машина: ")}{escape_md(car.brand)} {escape_md(car.model)} ({car.number_plate[:6]} {car.number_plate[6:]})'
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
                        f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}\n'
                    ),
                    md.text(
                        f'🚩Для уточнения маршрута перейдите по [ссылке]({data["route_link"]})'
                        if data.get("route_link") is not None
                        and data.get("route_link")
                        and len(data.get("route_link")) > 0
                        else ""
                    ),
                    md.text(f"\nОтправить свою заявку вы можете при помощи бота: {escape_md(bot_link)}"),
                    sep="\n",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

            if data.get("route_link") is not None:
                del data["route_link"]
            await RideRequestTable.add(post_message_id=post_in_channel.message_id, **data)

        elif message.text == "Редактировать":
            await state.reset_state()
            await CreateRideRequest.date.set()
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
        logger.critical(Loggers.APP.value, f"Ошибка {str(ex)}, функция: process_driver(создание заявки)")
