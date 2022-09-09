"""
This module for creating ride request
"""
from datetime import datetime, date, time
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
import emoji
import aiogram.utils.markdown as md
from src.packages.bot.loader import dispatcher, bot
from src.packages.loaders import env_variables
from src.packages.database import UserTable, RideRequestTable, CarTable
from src.packages.bot.keyboards import buttons
from src.packages.bot.states import CreateRideRequest
from src.packages.bot.filters import GroupMember, ChatWithABot, AuthorisedUser, HasCar

channel_id = env_variables.get("CHANNEL_ID")


def refactor_str(str_input):
    """
    This function refactor string
    @param str_input: str
    """
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0' + str_input}"


def handler_date(str_date):
    """
    This function refactor str in date
    @param str_date: str_date
    """
    lst_date = str_date.split(".")
    day = int(lst_date[0])
    month = int(lst_date[1])
    year = datetime.now().year
    return date(year, month, day)


def handler_time(str_time):
    """
    This function refactor str in time
    @param str_time: str_time
    """
    lst_time = str_time.split(":")
    hour = int(lst_time[0])
    minute = int(lst_time[1])
    second = 0
    return time(hour, minute, second)


@dispatcher.message_handler(state="*", commands="Отмена")
@dispatcher.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    This function to exit to the main menu
    @param message: Message object
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы в главном меню", reply_markup=buttons.main_menu_authorised)


@dispatcher.message_handler(
    ChatWithABot(), GroupMember(), AuthorisedUser(), HasCar(), Text(equals=["Создать заявку"], ignore_case=True)
)
async def choice_date(message: types.Message):
    """
    This function transition to the state create ride request and choice ride data
    @param message: Message object
    """
    await CreateRideRequest.date.set()
    await message.answer("Выерите дату " + emoji.emojize(":calendar:"), reply_markup=buttons.date_keyboard)


@dispatcher.message_handler(
    ChatWithABot(), GroupMember(), AuthorisedUser(), ~HasCar(), Text(equals=["Создать заявку"], ignore_case=True)
)
async def not_car(message: types.Message):
    """
    This function shows message use without car
    @param message: Message object
    """
    await message.answer(
        "Для создания заявки необходимо добавить машину в разделе 'Мой профиль'\n" "Нажмите на кнопку ниже",
        reply_markup=buttons.keyboard_main_profile,
    )


@dispatcher.message_handler(state=CreateRideRequest.date)
async def process_date(message: types.Message, state: FSMContext):
    """
    This function save ride data
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["date_ride"] = handler_date(message.text)
    await CreateRideRequest.next()
    await message.answer("Выберите время" + emoji.emojize(":alarm_clock:"), reply_markup=buttons.time_keyboard)


@dispatcher.message_handler(state=CreateRideRequest.time)
async def process_time(message: types.Message, state: FSMContext):
    """
    This function save ride time
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["time_ride"] = handler_time(message.text)
    await CreateRideRequest.next()
    await message.answer(
        "Введите условие довоза\n Например: 'за шоколадку' \n Или нажмите  'дальше'",
        reply_markup=buttons.keyboard_terms_delivery,
    )


@dispatcher.message_handler(state=CreateRideRequest.delivery_terms)
async def process_terms_delivery(message: types.Message, state: FSMContext):
    """
    This function save delivery terms
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["delivery_terms"] = message.text
    await CreateRideRequest.next()
    await message.answer(
        "Введите или выберите место отправления\nНапример:'Маркса 22'", reply_markup=buttons.keyboard_place_departure
    )


@dispatcher.message_handler(state=CreateRideRequest.place_departure)
async def process_place_departure(message: types.Message, state: FSMContext):
    """
    This function save departure place
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["departure_place"] = message.text
    await CreateRideRequest.next()
    await message.answer("Введите место прибытия\nНапример:'Маркса 22'", reply_markup=buttons.default_keyboard)


@dispatcher.message_handler(state=CreateRideRequest.place_comming)
async def process_place_comming(message: types.Message, state: FSMContext):
    """
    This function save destination place
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["destination_place"] = message.text
    await CreateRideRequest.next()
    await message.answer("Выберите количество мест:", reply_markup=buttons.number_of_seats_keyboard)


@dispatcher.message_handler(state=CreateRideRequest.number_of_seats)
async def process_number_of_seats(message: types.Message, state: FSMContext):
    """
    This function save seats number
    @param message: Message object
    @param state: FSMContext object
    """
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
                f'{md.bold("Водитель: ")}{user_from_db.first_name} {user_from_db.last_name if user_from_db.last_name is not None else ""} '  # pylint: disable=line-too-long
            ),
            md.text(
                f'{md.bold("Номер телефона: ")}'
                f'{user_from_db.phone_number if user_from_db.phone_number is not None else "не указан"}'
            ),
            md.text(f'{md.bold("Машина: ")}{car.brand} {car.model} ({car.number_plate})'),
            md.text(
                f'{md.bold("Когда и восколько: ")}{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'  # pylint: disable=line-too-long
                f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.{data["date_ride"].year if data.get("date_ride") is not None else ""} в '  # pylint: disable=line-too-long
                f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'  # pylint: disable=line-too-long
            ),
            md.text(
                f"{md.bold('Условия довоза: ')}"
                f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"  # pylint: disable=line-too-long
            ),
            md.text(
                f'{md.bold("Место отправления: ")}{data["departure_place"] if data.get("departure_place") is not None else ""}'  # pylint: disable=line-too-long
            ),
            md.text(
                f'{md.bold("Место прибытия: ")}{data["destination_place"] if data.get("destination_place") is not None else ""}'  # pylint: disable=line-too-long
            ),
            md.text(
                f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}'  # pylint: disable=line-too-long
            ),
            sep="\n",
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


@dispatcher.message_handler(state=CreateRideRequest.driver)
async def process_driver(message: types.Message, state: FSMContext):
    """
    This function save ride request
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Отправить":
        async with state.proxy() as data:
            user_from_db = await UserTable.get_by_telegram_id(message.from_user.id)
            print(user_from_db.id)
            data["author"] = user_from_db.id
        data = await state.get_data()
        await RideRequestTable.add(**data)
        car = await CarTable.get_by_user_id(user_from_db.id)
        await state.finish()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(f'{md.code("Заявка создана")}'),
                md.text(
                    f'{md.bold("Водитель: ")}{user_from_db.first_name} '
                    f'{user_from_db.last_name if user_from_db.last_name is not None else ""} '
                ),
                md.text(
                    f'{md.bold("Номер телефона: ")}'
                    f'{user_from_db.phone_number if user_from_db.phone_number is not None else "не указан"}'
                ),
                md.text(f'{md.bold("Машина: ")}{car.brand} {car.model} ({car.number_plate})'),
                md.text(
                    f'{md.bold("Когда и восколько: ")}'
                    f'{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'
                    f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.'
                    f'{data["date_ride"].year if data.get("date_ride") is not None else ""} в '
                    f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:'
                    f'{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'
                ),
                md.text(
                    f"{md.bold('Условия довоза: ')}"
                    f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Место отправления: ")}{data["departure_place"] if data.get("departure_place") is not None else ""}'  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Место прибытия: ")}{data["destination_place"] if data.get("destination_place") is not None else ""}'  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}'  # pylint: disable=line-too-long
                ),
                sep="\n",
            ),
            reply_markup=buttons.main_menu_authorised,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.send_message(message.chat.id, "Данную заявку вы сможете найти в нижнем меню -> «Мои заявки»")
        await bot.send_message(
            channel_id,
            md.text(
                md.text(f'{md.code("Заявка создана")}'),
                md.text(
                    f'{md.bold("Водитель: ")}{user_from_db.first_name} {user_from_db.last_name if user_from_db.last_name is not None else ""} '  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Номер телефона: ")}'
                    f'{user_from_db.phone_number if user_from_db.phone_number is not None else "не указан"}'
                ),
                md.text(f'{md.bold("Машина: ")}{car.brand} {car.model} ({car.number_plate})'),
                md.text(
                    f'{md.bold("Когда и восколько: ")}{refactor_str(data["date_ride"].day if data.get("date_ride") is not None else "")}.'  # pylint: disable=line-too-long
                    f'{refactor_str(data["date_ride"].month if data.get("date_ride") is not None else "")}.{data["date_ride"].year if data.get("date_ride") is not None else ""} в '  # pylint: disable=line-too-long
                    f'{refactor_str(data["time_ride"].hour if data.get("time_ride") is not None else "")}:{refactor_str(data["time_ride"].minute if data.get("time_ride") is not None else "")}'  # pylint: disable=line-too-long
                ),
                md.text(
                    f"{md.bold('Условия довоза: ')}"
                    f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' and data.get('delivery_terms') is not None else 'Не указано'}"  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Место отправления: ")}{data["departure_place"] if data.get("departure_place") is not None else ""}'  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Место прибытия: ")}{data["destination_place"] if data.get("destination_place") is not None else ""}'  # pylint: disable=line-too-long
                ),
                md.text(
                    f'{md.bold("Количество мест: ")}{data["seats_number"] if data.get("seats_number") is not None else ""}'  # pylint: disable=line-too-long
                ),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    elif message.text == "Редактировать":
        await state.reset_state()
        await CreateRideRequest.date.set()
        await message.answer("Выерите дату " + emoji.emojize(":calendar:"), reply_markup=buttons.date_keyboard)
    else:
        await state.finish()
        await message.answer("Вы в главном меню:", reply_markup=buttons.main_menu_authorised)
