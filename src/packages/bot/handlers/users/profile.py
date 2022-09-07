"""
This module handles users commands
"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.packages.database import DatabaseException
from src.packages.bot.states import EditProfileFSM, DeleteProfileFSM
from src.packages.bot.filters import GroupMember, ChatWithABot, AuthorisedUser
from src.packages.bot.loader import dispatcher
from src.packages.bot.keyboards import buttons
from src.packages.database import UserTable, TelegramProfileTable


# pylint:disable=W0511
# TODO: Отрефакторить строки с текстами сообщений


@dispatcher.message_handler(ChatWithABot(), GroupMember(), ~AuthorisedUser(), text=["Создать профиль"])
async def edit_start(message: types.Message):
    """
    This function starts EditProfileFSM
    @param message: Message object
    """
    await EditProfileFSM.first_name.set()
    await edit_first_name(message=message)


@dispatcher.message_handler(state=EditProfileFSM.first_name)
async def edit_first_name(message: types.Message):
    """
    This state function asks for user first name
    @param message: Message object
    """
    await message.answer(text="Введите ваше имя:")
    await EditProfileFSM.next()


@dispatcher.message_handler(state=EditProfileFSM.last_name)
async def edit_last_name(message: types.Message, state: FSMContext):
    """
    This state function asks for user last name
    @param message: Message object
    @param state: FSMContext object
    """
    await state.update_data(first_name=message.text)
    await message.answer(text="Введите вашу фамилию:")
    await EditProfileFSM.next()


@dispatcher.message_handler(state=EditProfileFSM.phone_number)
async def edit_phone_number(message: types.Message, state: FSMContext):
    """
    This state function asks for user phone number
    @param message: Message object
    @param state: FSMContext object
    """
    await state.update_data(last_name=message.text)
    await message.answer(text="Введите ваш номер телефона:")
    await EditProfileFSM.next()


@dispatcher.message_handler(state=EditProfileFSM.confirmation)
async def edit_confirmation(message: types.Message, state: FSMContext):
    """
    This state function gets user confirmation on his info
    @param message: Message object
    @param state: FSMContext object
    """
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    await message.answer(
        text=f"""Проверьте введённые данные:
Имя: {data.get("first_name")}
Фамилия: {data.get("last_name")}
Номер телефона: {data.get("phone_number")}
""",
        reply_markup=buttons.profile_data_confirmation,
    )
    await EditProfileFSM.next()


@dispatcher.message_handler(state=EditProfileFSM.result_handling)
async def edit_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after create confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    if message.text == "Всё верно":
        try:
            data = await state.get_data()
            nickname = message.from_user.username
            if nickname is None:
                nickname = str(message.from_user.id)

            await TelegramProfileTable.add(tg_id=message.from_user.id, nickname=nickname)
            await UserTable.add(
                tg_id=message.from_user.id,
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                car_id=None,
                phone_number=data.get("phone_number"),
            )
            await message.answer(text="Профиль успешно создан!")
        except DatabaseException as error:
            await message.answer(text=str(error))
        finally:
            await state.finish()
    elif message.text == "Хочу исправить":
        await state.finish()
        await message.answer(text="Давайте попробуем снова")
        await edit_start(message)
    elif message.text == "Отмена":
        await state.finish()
        await message.answer(text="Как будете готовы - возвращайтесь!")
    else:
        await state.finish()
        await message.answer(text="Что-то пошло не так, попробуйте ещё раз :(")


@dispatcher.message_handler(ChatWithABot(), GroupMember(), AuthorisedUser(), text=["Мой профиль"])
async def profile(message: types.Message):
    """
    This function shows user info
    @param message: Message object
    """
    user = await UserTable.get(message.from_user.id, id_type="telegram")
    await message.answer(
        text=f"""Ваш профиль:
{user.first_name} {user.last_name}
Телефон: {user.phone_number}
""",
        reply_markup=buttons.profile_menu,
    )


# pylint:disable=W0511
@dispatcher.message_handler(ChatWithABot(), GroupMember(), AuthorisedUser(), text=["Редактировать профиль"])
async def update_profile(message: types.Message):  # TODO: Нужен запрос к БД на обновление информации
    """
    This function shall start UpdateProfileFSM
    @param message: Message object
    """
    # pylint:disable=W0511
    await message.answer(text="Привет")  # TODO: Также подумать над реализацией изменения информации


@dispatcher.message_handler(ChatWithABot(), GroupMember(), AuthorisedUser(), text=["Удалить профиль"])
async def delete_start(message: types.Message):
    """
    This function starts DeleteProfileFSM
    @param message: Message object
    """
    await DeleteProfileFSM.confirmation.set()
    await message.answer(text="""Вы действительно хотите удалить профиль?""", reply_markup=buttons.profile_delete_menu)


@dispatcher.message_handler(state=DeleteProfileFSM.confirmation)
async def delete_result_handling(message: types.Message, state: FSMContext):
    """
    This state function handles user answer after delete confirmation question
    @param message: Message object
    @param state: FSMContext object
    """
    # pylint:disable=W0511
    if message.text == "Да":  # TODO: Нужен запрос к БД на удаление записей
        await UserTable.delete(message.from_user.id, id_type="telegram")
        await state.finish()
        await message.answer(text="Ваш профиль удалён, возвращайтесь поскорее!")
    elif message.text == "Отменить":
        await state.finish()
    else:
        await state.finish()
        await message.answer(text="Что-то пошло не так :(")
