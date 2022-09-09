"""
Module keeps methods to operate with database telegram profile table
"""
from asyncpg import UniqueViolationError
from src.packages.database.shemas import TgProfile
from ..database import DatabaseException


class TelegramProfileTable:
    """
    This class is to operate with database telegram profile table
    """

    @staticmethod
    async def add(tg_id: int, user_id: int, nickname: str):
        """
        The method adding a record to  table tg_profiles
        @param tg_id: id from telegram
        @param user_id: id from tables users
        @param nickname: nickname from telegram
        """
        try:
            tg_profile = TgProfile(tg_id=tg_id, user_id=user_id, nickname=nickname)
            await tg_profile.create()
        except UniqueViolationError as exception:
            raise DatabaseException("Профиль телеграмма уже существует в базе данных.") from exception

    @staticmethod
    async def get(tg_id: int) -> TgProfile:
        """
        The method selection tg_profile by tg_id from the table tg_profiles
        @param tg_id: User ID from telegram
        @return: tg_profile object from tg_profiles table
        """
        tg_profile = await TgProfile.query.where(TgProfile.tg_id == tg_id).gino.first()
        return tg_profile

    @classmethod
    async def update(cls, tg_id: int, **data):
        """
        The method change  nickname from tg_profile
        @param tg_id: User ID from telegram
        @param data: data to update
        @return: true if success else false
        """
        tg_profile = await cls.get(tg_id)
        if not tg_profile:
            return False
        await tg_profile.update(**data).apply()
        return True

    @classmethod
    async def delete(cls, tg_id: int):
        """
        This method deletes TelegramProfile object
        @param tg_id: User ID from telegram
        @return: true if success else false
        """
        tg_profile = await cls.get(tg_id)
        if not tg_profile:
            return False
        await tg_profile.delete()
        return True
