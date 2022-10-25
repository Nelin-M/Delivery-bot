"""
This module handles car profile commands
"""
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot, ChatWithABotCallback, GroupMemberCallback, HasCar
from src.packages.bot.keyboards import buttons, inline_buttons
from src.packages.bot.loader import dispatcher
from src.packages.bot.states import EditCarFSM, DeleteCarFSM
from src.packages.database import DatabaseException, UserTable, CarTable


@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Мой автомобиль"])
async def car_info_car_added(message: types.Message):
    """
    This function shows user info
    @param message: Message object
    """
    user = await UserTable.get_by_telegram_id(message.from_user.id)
    car = await CarTable.get_by_user_id(user.id)
    await message.answer(
        text=f"Ваш авто:" f"\n{car.brand} {car.model}" f"\n{car.number_plate}", reply_markup=buttons.car_added_menu
    )


@dispatcher.message_handler(ChatWithABot(), GroupMember(), ~HasCar(), text=["Мой автомобиль"])
async def car_info_no_car(message: types.Message):
    """
    This function shows user info
    @param message: Message object
    """
    await message.answer(
        text="Здесь вы можете добавить информацию о вашем авто, чтобы создавать заявки",
        reply_markup=inline_buttons.add_car_menu,
    )


@dispatcher.callback_query_handler(ChatWithABotCallback(), GroupMemberCallback(), text="Добавить автомобиль")
async def edit_start(message: types.Message):
    """
    This function starts EditProfileFSM
    @param message: Message object
    @param call: Callback query object
    """

    await EditCarFSM.brand.set()
    await edit_brand(message=message)


@dispatcher.callback_query_handler(state=EditCarFSM.brand)
async def edit_brand(message: types.Message):
    """
    This state function asks for user first name
    @param message: Message object
    @param call: Callback query object
    """
    if isinstance(message, types.CallbackQuery):
        await message.message.answer(
            text="Введите марку:",
            reply_markup=buttons.car_edit_cancel,
        )
    else:
        await message.answer(
            text="Введите марку:",
            reply_markup=buttons.car_edit_cancel,
        )
    await EditCarFSM.next()


@dispatcher.message_handler(state=EditCarFSM.model)
async def edit_model(message: types.Message, state: FSMContext):
    """
    This state function asks for user last name
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Отмена":
        await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
        return await state.finish()

    await state.update_data(brand=message.text)
    await message.answer(
        text="Введите модель:",
        reply_markup=buttons.car_edit_cancel,
    )
    await EditCarFSM.next()


@dispatcher.message_handler(state=EditCarFSM.number_plate)
async def edit_number_plate(message: types.Message, state: FSMContext):
    """
    This state function asks for user phone number
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Отмена":
        await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
        return await state.finish()

    await state.update_data(model=message.text)
    await message.answer(
        text="Введите гос. номер, в формате: серия, номер, серия, код региона (A000AA123)",
        reply_markup=buttons.car_edit_cancel,
    )
    await EditCarFSM.next()


@dispatcher.message_handler(state=EditCarFSM.confirmation)
async def edit_confirmation(message: types.Message, state: FSMContext):
    """
    This state function gets user confirmation on his info
    @param message: Message object
    @param state: FSMContext object
    """
    regexp = re.compile(r"^[АВЕКМНОРСТУХABEKMHOPCTYX]\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}(?P<reg>\d{2,3})$")
    car_id = message.text.upper().strip()
    match = regexp.match(car_id)

    if message.text == "Отмена":
        await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
        return await state.finish()

    if match:
        await state.update_data(number_plate=car_id)
        data = await state.get_data()
        await message.answer(
            text=f"Проверьте введённые данные:"
            f"\nМарка: {data.get('brand')}"
            f"\nМодель: {data.get('model')}"
            f"\nГос.номер: {data.get('number_plate')[:6]} {data.get('number_plate')[6:]}",
            reply_markup=buttons.car_create_confirmation_keyboard,
        )
        await EditCarFSM.next()
    elif match is None:
        await message.answer(
            text="Гос. номер введен неверно, повторите ввод, в формате: серия, номер, серия, " "код региона (A000AA123)"
        )


@dispatcher.message_handler(~HasCar(), state=EditCarFSM.result_handling)
async def create_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after create confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    # pylint: disable=R0801
    if message.text == "Всё верно":
        try:
            data = await state.get_data()
            user = await UserTable.get_by_telegram_id(message.from_user.id)
            car_id = await CarTable.add(
                model=data.get("model"), brand=data.get("brand"), number_plate=data.get("number_plate"), user_id=user.id
            )
            await UserTable.update(user_id=user.id, data={"car_id": car_id})
            await message.answer(text="Автомобиль успешно добавлен!", reply_markup=buttons.main_menu_authorised)
        # pylint: disable=R0801
        except DatabaseException as error:
            await message.answer(text=str(error))
        finally:
            await state.finish()
    elif message.text == "Хочу исправить":
        await state.finish()
        await message.answer(text="Давайте попробуем снова", reply_markup=buttons.main_menu_authorised)
        await edit_start(message=message)
    elif message.text == "Отмена":
        await state.finish()
        await message.answer(text="Как будете готовы - возвращайтесь!", reply_markup=buttons.main_menu_authorised)
    else:
        await state.finish()
        await message.answer(
            text="Что-то пошло не так, попробуйте ещё раз :(", reply_markup=buttons.main_menu_authorised
        )


@dispatcher.message_handler(HasCar(), state=EditCarFSM.result_handling)
async def edit_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after create confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    # pylint: disable=R0801
    if message.text == "Всё верно":
        try:
            data = await state.get_data()
            user = await UserTable.get_by_telegram_id(message.from_user.id)
            await CarTable.update(car_id=user.car_id, data=data)
            await message.answer(text="Автомобиль успешно изменён!", reply_markup=buttons.main_menu_authorised)
        # pylint: disable=R0801
        except DatabaseException as error:
            await message.answer(text=str(error))
        finally:
            await state.finish()
    elif message.text == "Хочу исправить":
        await state.finish()
        await message.answer(text="Давайте попробуем снова")
        await edit_start(message=message)
    elif message.text == "Отмена":
        await state.finish()
        await message.answer(text="Как будете готовы - возвращайтесь!", reply_markup=buttons.main_menu_authorised)
    else:
        await state.finish()
        await message.answer(
            text="Что-то пошло не так, попробуйте ещё раз :(", reply_markup=buttons.main_menu_authorised
        )


# pylint:disable=W0511
@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Редактировать автомобиль"])
async def update_car_info(message: types.Message):
    """
    This function shall start UpdateProfileFSM
    @param message: Message object
    """
    # pylint:disable=W0511
    await edit_start(message=message)


@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Удалить автомобиль"])
async def delete_start(message: types.Message):
    """
    This function starts DeleteProfileFSM
    @param message: Message object
    """
    await DeleteCarFSM.confirmation.set()
    await message.answer(
        text="Вы действительно хотите удалить данный автомобиль?", reply_markup=buttons.car_delete_confirmation
    )


@dispatcher.message_handler(state=DeleteCarFSM.confirmation)
async def delete_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after delete confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Да":
        user = await UserTable.get_by_telegram_id(message.from_user.id)
        await CarTable.delete(user.car_id)
        await UserTable.update(user_id=user.id, data={"car_id": None})
        await state.finish()
        await message.answer(
            text="Ваш автомобиль удалён, чтобы пользоваться сервисом без ограничений, создайте новый в меню",
            reply_markup=buttons.main_menu_authorised,
        )
    # pylint: disable=R0801
    elif message.text == "Отменить":
        await state.finish()
        await message.answer(text="Как будете готовы - возвращайтесь!", reply_markup=buttons.main_menu_authorised)
    else:
        await state.finish()
        await message.answer(
            text="Что-то пошло не так, попробуйте ещё раз :(", reply_markup=buttons.main_menu_authorised
        )
