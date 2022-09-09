"""
Module keeps methods to operate with database user table
"""
from asyncpg import UniqueViolationError
from src.packages.database.shemas import User
from ..database import DatabaseException


class UserTable:
    """
    This class is to operate with database user table
    """

    @staticmethod
    async def add(id_from_tg: int, first_name: str, last_name: str, id_from_car: int or None, phone_number: str):
        """
        The method to add a record to a table users
        @param id_from_tg: id from telegram
        @param first_name: first_name from telegram
        @param last_name: last_name from telegram
        @param id_from_car: car_id from cars table
        @param phone_number: phone number entered by the user
        @return: id of the user added to the table users
        """
        try:
            user = User(
                id_from_tg=id_from_tg,
                first_name=first_name,
                last_name=last_name,
                id_from_car=id_from_car,
                phone_number=phone_number,
            )
            await user.create()
            return user
        except UniqueViolationError as exception:
            raise DatabaseException("Пользователь уже существует в базе данных.") from exception

    # pylint: disable=W0622,C0103:
    @staticmethod
    async def get_by_user_id(user_id: int) -> User:
        """
        This method returns User object
        @param user_id: User.id
        @return: User
        """
        # try:
        user = await User.query.where(User.id == user_id).gino.first()
        # except:
        #     pass

        return user

    @staticmethod
    async def get_by_telegram_id(id_from_tg: int) -> User:
        """
        This method returns User object
        @param id_from_tg: telegram id
        @return: User
        """
        # try:
        user = await User.query.where(User.id_from_tg == id_from_tg).gino.first()
        # except:
        #     pass

        return user

    # pylint: disable=W0622,C0103:
    @classmethod
    async def update(cls, user_id: int, data):
        """
        This method updates User object
        @param user_id: User.id
        @param data: data to update
        @return:
        """
        # try:
        user = await cls.get_by_user_id(user_id)
        await user.update(**data).apply()
        # except:
        #     pass

    # pylint: disable=W0622,C0103:
    @classmethod
    async def delete(cls, user_id: int):
        """
        This method deletes User object
        @param user_id: User.id
        @return:
        """
        # try:
        user = await cls.get_by_user_id(user_id)
        await user.delete()
        # except:
        #     pass
