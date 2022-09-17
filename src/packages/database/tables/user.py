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
    async def add(id_from_tg: int, id_from_car: int or None):
        """
        The method to add a record to a table users
        @param id_from_tg: id from telegram
        @param id_from_car: car_id from cars table
        @return: id of the user added to the table users
        """
        try:
            user = User(id_from_tg=id_from_tg, id_from_car=id_from_car)
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
        user = await User.query.where(User.id == user_id).gino.first()
        return user

    @staticmethod
    async def get_by_telegram_id(id_from_tg: int) -> User:
        """
        This method returns User object
        @param id_from_tg: telegram id
        @return: User
        """
        user = await User.query.where(User.id_from_tg == id_from_tg).gino.first()
        return user

    # pylint: disable=W0622,C0103:
    @classmethod
    async def update(cls, user_id: int, data: dict):
        """
        This method updates User object
        @param user_id: User.user_id
        @param data: data to update
        @return:
        """
        user = await cls.get_by_user_id(user_id)
        await user.update(**data).apply()

    # pylint: disable=W0622,C0103:
    @classmethod
    async def delete(cls, user_id: int):
        """
        This method deletes User object
        @param user_id: User.id
        @return:
        """
        user = await cls.get_by_user_id(user_id)
        await user.delete()
