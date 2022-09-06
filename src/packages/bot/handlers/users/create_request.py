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
from src.packages.database import database
from src.packages.bot.keyboards.buttons.choice_time import time_keyboard
from src.packages.bot.keyboards.buttons.choice_date import date_keyboard
from src.packages.bot.keyboards.buttons.destination_place import default_keyboard
from src.packages.bot.keyboards.buttons.departure_place import keyboard_place_departure
from src.packages.bot.keyboards.buttons.delivery_terms import keyboard_terms_delivery
from src.packages.bot.keyboards.buttons.seats_number import number_of_seats_keyboard
from src.packages.bot.keyboards.buttons.main_menu import main_menu_authorised
from src.packages.bot.keyboards.buttons.confirmation_ride_request import keyboard_ok
from src.packages.bot.states.create_request import RideRequest

channel_id = env_variables.get("CHANNEL_ID")


####################################################################
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


@dispatcher.message_handler(Text(equals="В главное меню", ignore_case=True))
async def menu_handler(message: types.Message):
    """
    This function return to the main menu
    @param message: Message object
    """
    await message.answer("Вы в главном меню:", reply_markup=main_menu_authorised)


@dispatcher.message_handler(Text(equals=["Создать заявку"], ignore_case=True))
async def choice_date(message: types.Message):
    """
    This function transition to the state create ride request and choice ride data
    @param message: Message object
    """
    await database.connect_db()
    await RideRequest.date.set()
    await message.answer("Выерите дату " + emoji.emojize(":calendar:"), reply_markup=date_keyboard)


@dispatcher.message_handler(state=RideRequest.date)
async def process_date(message: types.Message, state: FSMContext):
    """
    This function save ride data
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["date_ride"] = handler_date(message.text)
    await RideRequest.next()
    await message.answer("Выберите время" + emoji.emojize(":alarm_clock:"), reply_markup=time_keyboard)


@dispatcher.message_handler(state=RideRequest.time)
async def process_time(message: types.Message, state: FSMContext):
    """
    This function save ride time
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["time_ride"] = handler_time(message.text)
    await RideRequest.next()
    await message.answer(
        "Введите условие довоза\n Например: 'за шоколадку' \n Или нажмите  'дальше'",
        reply_markup=keyboard_terms_delivery,
    )


@dispatcher.message_handler(state=RideRequest.delivery_terms)
async def process_terms_delivery(message: types.Message, state: FSMContext):
    """
    This function save delivery terms
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["delivery_terms"] = message.text
    await RideRequest.next()
    await message.answer(
        "Введите или выберите место отправления\nНапример:'Маркса 22'", reply_markup=keyboard_place_departure
    )


@dispatcher.message_handler(state=RideRequest.place_departure)
async def process_place_departure(message: types.Message, state: FSMContext):
    """
    This function save departure place
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["departure_place"] = message.text
    await RideRequest.next()
    await message.answer("Введите место прибытия\nНапример:'Маркса 22'", reply_markup=default_keyboard)


@dispatcher.message_handler(state=RideRequest.place_comming)
async def process_place_comming(message: types.Message, state: FSMContext):
    """
    This function save destination place
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["destination_place"] = message.text
    await RideRequest.next()
    await message.answer("Выберите количество мест:", reply_markup=number_of_seats_keyboard)


@dispatcher.message_handler(state=RideRequest.number_of_seats)
async def process_number_of_seats(message: types.Message, state: FSMContext):
    """
    This function save seats number
    @param message: Message object
    @param state: FSMContext object
    """
    async with state.proxy() as data:
        data["seats_number"] = int(message.text)
    await RideRequest.next()
    await message.answer(
        "Подтвердите создание заявки  " + emoji.emojize(":check_mark_button:"), reply_markup=keyboard_ok
    )
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text(
                f'{md.bold("Когда и восколько: ")}{refactor_str(data["date_ride"].day)}.'
                f'{refactor_str(data["date_ride"].month)}.{data["date_ride"].year} в '
                f'{refactor_str(data["time_ride"].hour)}:{refactor_str(data["time_ride"].minute)}'
            ),
            md.text(
                f"{md.bold('Условия довоза: ')}"
                f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' else 'Не указано'}"
            ),
            md.text(f'{md.bold("Место отправления: ")}{data["departure_place"]}'),
            md.text(f'{md.bold("Место прибытия: ")}{data["destination_place"]}'),
            md.text(f'{md.bold("Количество мест: ")}{data["seats_number"]}'),
            sep="\n",
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


@dispatcher.message_handler(state=RideRequest.driver)
async def process_driver(message: types.Message, state: FSMContext):
    """
    This function save ride request
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Отправить":
        async with state.proxy() as data:
            user_from_db = await database.select_user_by_tg_id(message.from_user.id)
            data["author"] = user_from_db.id
        data = await state.get_data()
        await database.add_ride_request(**data)
        car = await database.select_car_by_id(user_from_db.car_id)
        await state.finish()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(f'{md.code("Заявка создана")}'),
                md.text(f'{md.bold("Водитель: ")}{user_from_db.first_name} {user_from_db.last_name} '),
                md.text(
                    f'{md.bold("Номер телефона: ")}'
                    f'{user_from_db.phone_number if user_from_db.phone_number is not None else "не указан"}'
                ),
                md.text(f'{md.bold("Машина: ")}{car.brand} {car.model} ({car.number_plate})'),
                md.text(
                    f'{md.bold("Когда и восколько: ")}{refactor_str(data["date_ride"].day)}.'
                    f'{refactor_str(data["date_ride"].month)}.{data["date_ride"].year} в '
                    f'{refactor_str(data["time_ride"].hour)}:{refactor_str(data["time_ride"].minute)}'
                ),
                md.text(
                    f"{md.bold('Условия довоза: ')}"
                    f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' else 'Не указано'}"
                ),
                md.text(f'{md.bold("Место отправления: ")}{data["departure_place"]}'),
                md.text(f'{md.bold("Место прибытия: ")}{data["destination_place"]}'),
                md.text(f'{md.bold("Количество мест: ")}{data["seats_number"]}'),
                sep="\n",
            ),
            reply_markup=main_menu_authorised,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.send_message(
            channel_id,
            md.text(
                md.text(f'{md.code("Заявка создана")}'),
                md.text(f'{md.bold("Водитель: ")}{user_from_db.first_name} {user_from_db.last_name} '),
                md.text(
                    f'{md.bold("Номер телефона: ")}'
                    f'{user_from_db.phone_number if user_from_db.phone_number is not None else "не указан"}'
                ),
                md.text(f'{md.bold("Машина: ")}{car.brand} {car.model} ({car.number_plate})'),
                md.text(
                    f'{md.bold("Когда и во сколько: ")}{refactor_str(data["date_ride"].day)}.'
                    f'{refactor_str(data["date_ride"].month)}.{data["date_ride"].year} в '
                    f'{refactor_str(data["time_ride"].hour)}:{refactor_str(data["time_ride"].minute)}'
                ),
                md.text(
                    f"{md.bold('Условия довоза: ')}"
                    f"{data['delivery_terms'] if data['delivery_terms'] != 'Дальше' else 'Не указано'}"
                ),
                md.text(f'{md.bold("Место отправления: ")}{data["departure_place"]}'),
                md.text(f'{md.bold("Место прибытия: ")}{data["destination_place"]}'),
                md.text(f'{md.bold("Количество мест: ")}{data["seats_number"]}'),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await state.finish()
        await message.answer("Вы в главном меню:", reply_markup=main_menu_authorised)
