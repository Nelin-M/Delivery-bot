"""
This module handles car profile commands
"""
# pylint:disable=broad-except
import re
import inspect

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot, ChatWithABotCallback, GroupMemberCallback, HasCar
from src.packages.bot.keyboards import buttons, inline_buttons
from src.packages.bot.loader import dispatcher
from src.packages.bot.states import EditCarFSM, DeleteCarFSM
from src.packages.database import DatabaseException, UserTable, CarTable, TelegramProfileTable
from src.packages.logger import logger, Loggers


@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Мой автомобиль"])
async def car_info_car_added(message: types.Message):
    """
    This function shows user info
    @param message: Message object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        try:
            user = await UserTable.get_by_telegram_id(message.from_user.id)
        except DatabaseException:
            logger.critical_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                'пользователь отсутствует в базе, нажал кнопку "Мой автомобиль"',
            )

            user = await UserTable.add(tg_id=message.from_user.id, car_id=None)
            await TelegramProfileTable.add(
                tg_id=message.from_user.id, user_id=user.id, nickname=message.from_user.username
            )
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "Пользователь добавлен в базу"
            )
        try:
            car = await CarTable.get_by_user_id(user.id)
        except DatabaseException:
            logger.error_from_handlers(Loggers.APP.value, tg_user_id, name_func, message_from_user, "авто нет в базе")
        await message.answer(
            text=f"Ваш авто:" f"\n{car.brand} {car.model}" f"\n{car.number_plate}", reply_markup=buttons.car_added_menu
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: car_info_car_added")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text=["Мой автомобиль"])
async def car_info_no_car(message: types.Message):
    """
    This function shows user info
    @param message: Message object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await message.answer(
            text="Здесь вы можете добавить информацию о вашем авто, чтобы создавать заявки",
            reply_markup=inline_buttons.add_car_menu,
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: car_info_no_car")


@dispatcher.callback_query_handler(ChatWithABotCallback(), GroupMemberCallback(), text="Добавить автомобиль")
async def edit_start(call: types.CallbackQuery):
    """
    This function starts EditProfileFSM
    @param call: CallbackQuery object
    """
    try:
        tg_user_id = dict(call).get("from").get("id")
        message_from_user = dict(call).get("data")
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await EditCarFSM.brand.set()
        logger.info_from_handlers(
            Loggers.APP.value, tg_user_id, name_func, message_from_user, "Начало состояния добавления авто"
        )
        await edit_brand(message=call)
        try:
            await call.answer()
        except TypeError as ex:
            logger.warning_from_handlers(Loggers.APP.value, tg_user_id, name_func, message_from_user, f"{ex}")
    except Exception as ex:
        await call.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_start(добавление авто)")


@dispatcher.callback_query_handler(state=EditCarFSM.brand)
async def edit_brand(message: types.Message):
    """
    This state function asks for user first name
    @param message: Message object
    """
    try:
        tg_user_id = dict(message).get("from").get("id")
        message_from_user = dict(message).get("data")
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
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
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_brand")


@dispatcher.message_handler(state=EditCarFSM.model)
async def edit_model(message: types.Message, state: FSMContext):
    """
    This state function asks for user last name
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Отмена":
            await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
            logger.info_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "В главном меню, завершение состояния (добавление автомобиля)",
            )
            return await state.finish()
        await state.update_data(brand=message.text)
        logger.info_from_handlers(
            Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "изменил бренд машины"
        )
        await message.answer(
            text="Введите модель:",
            reply_markup=buttons.car_edit_cancel,
        )
        await EditCarFSM.next()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_model")


@dispatcher.message_handler(state=EditCarFSM.number_plate)
async def edit_number_plate(message: types.Message, state: FSMContext):
    """
    This state function asks for user phone number
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Отмена":
            await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
            logger.info_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "В главном меню, завершение состояния (добавление автомобиля)",
            )
            return await state.finish()
        await state.update_data(model=message.text)
        logger.info_from_handlers(Loggers.APP.value, tg_user_id, name_func, message_from_user, "изменил модель машины")
        await message.answer(
            text="Введите гос. номер, в формате: серия, номер, серия, код региона (A000AA123)",
            reply_markup=buttons.car_edit_cancel,
        )
        await EditCarFSM.next()
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_number_plate")


@dispatcher.message_handler(state=EditCarFSM.confirmation)
async def edit_confirmation(message: types.Message, state: FSMContext):
    """
    This state function gets user confirmation on his info
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        regexp = re.compile(r"^[АВЕКМНОРСТУХABEKMHOPCTYX]\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}(?P<reg>\d{2,3})$")
        car_id = message.text.upper().strip()
        match = regexp.match(car_id)

        if message.text == "Отмена":
            await message.answer(text="Вы в главном меню", reply_markup=buttons.main_menu_authorised)
            logger.info_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "В главном меню, завершение состояния (добавление автомобиля)",
            )
            return await state.finish()

        if match:
            await state.update_data(number_plate=car_id)
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "изменил номер машины на"
            )
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
                text="Гос. номер введен неверно, повторите ввод, в формате: серия, номер, серия, "
                "код региона (A000AA123). "
            )
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "неверно ввел номер машины"
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_confirmation")


@dispatcher.message_handler(~HasCar(), state=EditCarFSM.result_handling)
async def create_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after create confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        # pylint: disable=R0801
        if message.text == "Всё верно":
            try:
                data = await state.get_data()
                user = await UserTable.get_by_telegram_id(message.from_user.id)
                car_id = await CarTable.add(
                    model=data.get("model"),
                    brand=data.get("brand"),
                    number_plate=data.get("number_plate"),
                    user_id=user.id,
                )
                await UserTable.update(user_id=user.id, data={"car_id": car_id})
                await message.answer(text="Автомобиль успешно добавлен!", reply_markup=buttons.main_menu_authorised)
                logger.info_from_handlers(
                    Loggers.APP.value,
                    tg_user_id,
                    name_func,
                    message_from_user,
                    f"успешно добавил авто "
                    f"model:{data.get('model')} brand:{data.get('brand')} "
                    f"number_plate:{data.get('number_plate')}",
                )
            # pylint: disable=R0801
            except DatabaseException as error:
                await message.answer(text=str(error))
                logger.error_from_handlers(
                    Loggers.APP.value,
                    tg_user_id,
                    name_func,
                    message_from_user,
                    f"ошибка при добавлении/обновлении авто {str(error)}",
                )
            finally:
                await state.finish()
        elif message.text == "Хочу исправить":
            await state.finish()
            await message.answer(text="Давайте попробуем снова", reply_markup=buttons.main_menu_authorised)
            await edit_start(call=message)
            logger.info_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "переход в состояние добавление/исправление авто",
            )
        elif message.text == "Отмена":
            await state.finish()
            await message.answer(text="Как будете готовы - возвращайтесь!", reply_markup=buttons.main_menu_authorised)
            logger.info_from_handlers(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "завершение состояния добавление/исправление авто",
            )
        else:
            await state.finish()
            await message.answer(
                text="Что-то пошло не так, попробуйте ещё раз :(", reply_markup=buttons.main_menu_authorised
            )
            logger.warning(
                Loggers.APP.value,
                tg_user_id,
                name_func,
                message_from_user,
                "возникла ошибка при добавлении/обновлении авто ",
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: create_result_handling")


@dispatcher.message_handler(HasCar(), state=EditCarFSM.result_handling)
async def edit_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after create confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        # pylint: disable=R0801
        if message.text == "Всё верно":
            try:
                data = await state.get_data()
                user = await UserTable.get_by_telegram_id(message.from_user.id)
                await CarTable.update(car_id=user.car_id, data=data)
                await message.answer(text="Автомобиль успешно изменён!", reply_markup=buttons.main_menu_authorised)
                logger.info_from_handlers(
                    Loggers.APP.value, tg_user_id, name_func, message_from_user, f"успешно изменил авто на {data}"
                )
            # pylint: disable=R0801
            except DatabaseException as error:
                await message.answer(text=str(error))
                logger.error_from_handlers(
                    Loggers.APP.value,
                    tg_user_id,
                    name_func,
                    message_from_user,
                    f"ошибка при редактировании авто {str(error)}",
                )
            finally:
                await state.finish()
        elif message.text == "Хочу исправить":
            await state.finish()
            await message.answer(text="Давайте попробуем снова")
            await edit_start(call=message)
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "старт состояния редактирование авто "
            )
        elif message.text == "Отмена":
            await state.finish()
            logger.info_from_handlers(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "завершение состояния редактирование авто "
            )
            await message.answer(text="Как будете готовы - возвращайтесь!", reply_markup=buttons.main_menu_authorised)
        else:
            await state.finish()
            await message.answer(
                text="Что-то пошло не так, попробуйте ещё раз :(", reply_markup=buttons.main_menu_authorised
            )
            logger.warning(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "возникла ошибка при редактировании авто"
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: edit_result_handling")


# pylint:disable=W0511
@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Редактировать автомобиль"])
async def update_car_info(message: types.Message):
    """
    This function shall start UpdateProfileFSM
    @param message: Message object
    """
    # pylint:disable=W0511
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await edit_start(call=message)
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: update_car_info")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), HasCar(), text=["Удалить автомобиль"])
async def delete_start(message: types.Message):
    """
    This function starts DeleteProfileFSM
    @param message: Message object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        await DeleteCarFSM.confirmation.set()
        await message.answer(
            text="Вы действительно хотите удалить данный автомобиль?", reply_markup=buttons.car_delete_confirmation
        )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: delete_start")


@dispatcher.message_handler(state=DeleteCarFSM.confirmation)
async def delete_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after delete confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    try:
        tg_user_id = message.from_user.id
        message_from_user = message.text
        name_func = inspect.getframeinfo(inspect.currentframe()).function
        logger.info_from_handlers(Loggers.INCOMING.value, tg_user_id, name_func, message_from_user)
        if message.text == "Да":
            user = await UserTable.get_by_telegram_id(message.from_user.id)
            await CarTable.delete(user.car_id)
            await UserTable.update(user_id=user.id, data={"car_id": None})
            await state.finish()
            logger.info_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "завершение состояния удаления авто"
            )
            await message.answer(
                text="Ваш автомобиль удалён, чтобы пользоваться сервисом без ограничений, создайте новый в меню",
                reply_markup=buttons.main_menu_authorised,
            )
            logger.info_from_handlers(
                Loggers.INCOMING.value, tg_user_id, name_func, message_from_user, "автомобиль удален"
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
            logger.warning(
                Loggers.APP.value, tg_user_id, name_func, message_from_user, "возникла ошибка при удалении авто"
            )
    except Exception as ex:
        await message.answer(
            "По техническим причинам, мы не смогли обработать ваш запрос, попробуйте позже",
            reply_markup=buttons.main_menu_authorised,
        )
        logger.critical(Loggers.APP.value, f"Ошибка{str(ex)}, функция: delete_result_handling")
