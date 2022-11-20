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
    async def add(tg_id: int, car_id: int or None):
        """
        The method to add a record to a table users
        @param tg_id: id from telegram
        @param car_id: car_id from cars table
        @return: id of the user added to the table users
        """
        try:
            user = User(tg_id=tg_id, car_id=car_id)
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
        if user is None:
            raise DatabaseException("Пользователь не найден в базе данных")
        return user

    @staticmethod
    async def get_by_telegram_id(tg_id: int) -> User:
        """
        This method returns User object
        @param tg_id: telegram id
        @return: User
        """

        user = await User.query.where(User.tg_id == tg_id).gino.first()
        if user is None:
            raise DatabaseException("Пользователь не найден в базе данных")
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
