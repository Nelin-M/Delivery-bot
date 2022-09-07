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
    async def add(tg_id: int, first_name: str, last_name: str, car_id: int, phone_number: str):
        """
        The method to add a record to a table users
        @param tg_id: id from telegram
        @param first_name: first_name from telegram
        @param last_name: last_name from telegram
        @param car_id: car_id from cars table
        @param phone_number: phone number entered by the user
        @return: id of the user added to the table users
        """
        try:
            user = User(
                tg_id=tg_id, first_name=first_name, last_name=last_name, car_id=car_id, phone_number=phone_number
            )
            await user.create()
        except UniqueViolationError as exception:
            raise DatabaseException("Пользователь уже существует в базе данных.") from exception

    # pylint: disable=W0622,C0103:
    @staticmethod
    async def get(id: int, id_type="table") -> User:
        """
        This method returns User object
        @param id: table row id or user's telegram id
        @param id_type: optional("table", "telegram")
        @return: User
        """
        user = None
        # try:
        if id_type == "table":
            user = await User.query.where(User.id == id).gino.first()
        elif id_type == "telegram":
            user = await User.query.where(User.tg_id == id).gino.first()
        # except:
        #     pass

        return user

    # pylint: disable=W0622,C0103:
    @classmethod
    async def update(cls, id: int, id_type="table", **data):
        """
        This method updates User object
        @param id: table row id or user's telegram id
        @param id_type: optional("table", "telegram")
        @param data: data to update
        @return:
        """
        # try:
        user = await cls.get(id, id_type)
        await user.update(**data).apply()
        # except:
        #     pass

    # pylint: disable=W0622,C0103:
    @classmethod
    async def delete(cls, id: int, id_type="table"):
        """
        This method deletes User object
        @param id: table row id or user's telegram id
        @param id_type: optional("table", "telegram")
        @return:
        """
        # try:
        user = await cls.get(id, id_type)
        await user.delete()
        # except:
        #     pass
