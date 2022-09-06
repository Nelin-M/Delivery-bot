"""
    The file contains commands for working with the database
"""
from typing import List
from datetime import date, time
from asyncpg import UniqueViolationError
from src.packages.database.shemas import User, RideRequest, Car, TgProfile, db
from src.packages.logger import Loggers, logger
from src.packages.loaders import env_variables

__all__ = ["Database"]


class DatabaseException(Exception):
    """
    Class-exception for any errors with database working.
    """


# pylint: disable=R0904:
class Database:
    """
    Database class.The class contains the necessary
    methods for working with the postgres sql database.
    """

    def __init__(self):
        self.host = env_variables.get("POSTGRES_HOST")
        self.user = env_variables.get("POSTGRES_DB")
        self.password = env_variables.get("POSTGRES_USER")
        self.db_name = env_variables.get("POSTGRES_PASSWORD")
        self.port = env_variables.get("POSTGRES_PORT", default=5432)

    async def connect_db(self):
        """
        method to connect to postgres database
        """
        try:
            await db.set_bind(
                f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            )
        # pylint: disable=W0703:
        except Exception as exception:
            logger.critical(Loggers.APP.value, f"Unexpected error: {exception}")

    @staticmethod
    # pylint: disable=W0238:
    async def __drop_tables():
        await db.gino.drop_all()

    @staticmethod
    # pylint: disable=W0238:
    async def __create_tables():
        await db.gino.create_all()

    @staticmethod
    async def add_user(tg_id: int, first_name: str, last_name: str, car_id: int, phone_number: str) -> int:
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
            return user.id
        except UniqueViolationError as exception:
            raise DatabaseException("Пользователь уже существует в базе данных.") from exception

    @staticmethod
    async def add_tg_profile(tg_id: int, nickname: str):
        """
        The method adding a record to  table tg_profiles
        @param tg_id: id from telegram
        @param nickname: nickname from telegram
        """
        try:
            tg_profile = TgProfile(tg_id=tg_id, nickname=nickname)
            await tg_profile.create()
        except UniqueViolationError as exception:
            raise DatabaseException("Профиль телеграмма уже существует в базе данных.") from exception

    @staticmethod
    async def add_car(model: str, brand: str, number_plate: str) -> int:
        """
        The method adding a record to table cars
        @param model: the model of car
        @param brand: the brand of car
        @param number_plate: the number_plate of car
        @return: id of the car added to the table cars
        """
        try:
            car = Car(model=model, brand=brand, number_plate=number_plate)
            car = await car.create()
            return car.id
        except UniqueViolationError as exception:
            raise DatabaseException("Автомобиль уже существует в базе данных.") from exception

    @staticmethod
    async def select_car_by_id(car_id: int) -> Car:
        """
        The method selection car by id from the table cars
        @param car_id: car id
        @return: car object from cars table
        """
        car = await Car.query.where(Car.id == car_id).gino.first()
        return car

    # pylint:disable=R0913
    @staticmethod
    async def add_ride_request(
        author: int,
        delivery_terms: str,
        date_ride: date,
        time_ride: time,
        departure_place: str,
        destination_place: str,
        seats_number: int,
    ) -> int:
        """
        The method adding a record to  table ride_requests
        @param author: user id from users table
        @param delivery_terms:delivery_terms
        @param date_ride:date
        @param time_ride:time
        @param departure_place:departure_place
        @param destination_place:destination_place
        @param seats_number: number of seats places
        @return: id of the ride request added to the table
        """
        try:
            new_request = RideRequest(
                author=author,
                delivery_terms=delivery_terms,
                date=date_ride,
                time=time_ride,
                departure_place=departure_place,
                destination_place=destination_place,
                seats_number=seats_number,
            )
            await new_request.create()
            return new_request.id
        except UniqueViolationError as exception:
            raise DatabaseException("Запрос на поездку уже существует в базе данных.") from exception

    @staticmethod
    async def select_all_requests() -> List[RideRequest]:
        """
        The method selects all records from the ride_requests table
        @return: list of RideRequest objects
        """
        ride_requests_all = await RideRequest.query.gino.all()
        return ride_requests_all

    @staticmethod
    async def select_all_users() -> List[User]:
        """
        The method selects all records from the users table
        @return: list of User objects
        """
        users = await User.query.gino.all()
        return users

    @staticmethod
    async def select_all_cars() -> List[Car]:
        """
        The method selects all records from the cars table
        @return: list of Car objects
        """
        cars = await Car.query.gino.all()
        return cars

    @staticmethod
    async def count_users() -> int:
        """
        The method to count the number of users in the users table
        @return: count users
        """
        count = await db.func.count(User.id).gino.scalar()
        return count

    @staticmethod
    async def count_ride_requests() -> int:
        """
        The method to count the number of ride_request in the ride_request table
        @return: count ride requests
        """
        count = await db.func.count(RideRequest.id).gino.scalar()
        return count

    @staticmethod
    async def count_cars() -> int:
        """
        The method to count the number of car in the cars table
        @return: count cars
        """
        count = await db.func.count(Car.tg_id).gino.scalar()
        return count

    @staticmethod
    async def count_tg_profiles() -> int:
        """
        The method to count the number of tg_profile in the tg_profiles table
        @return: count tg_profiles
        """
        count = await db.func.count(TgProfile.tg_id).gino.scalar()
        return count

    @staticmethod
    async def select_user(user_id: int) -> User:
        """
        The method selection user by id from the table
        @param user_id: User ID
        @return: user object from users table
        """
        user = await User.query.where(User.id == user_id).gino.first()
        return user

    @staticmethod
    async def select_user_by_tg_id(tg_id: int) -> User:
        """
        The method selection user by telegram_id from the table
        @param tg_id: User ID from telegram
        @return: user object from users table
        """
        user = await User.query.where(User.tg_id == tg_id).gino.first()
        return user

    @staticmethod
    async def select_tg_profile_by_tg_id(tg_id: int) -> TgProfile:
        """
        The method selection tg_profile by tg_id from the table tg_profiles
        @param tg_id: User ID from telegram
        @return: tg_profile object from tg_profiles table
        """
        tg_profile = await TgProfile.query.where(TgProfile.tg_id == tg_id).gino.first()
        return tg_profile

    async def select_nickname_from_tg_profile_by_tg_id(self, tg_id: int) -> str:
        """
        The method selection nickname from tg_profile by tg_id from the table tg_profiles
        @param tg_id: User ID from telegram
        @return: nickname
        """
        tg_profile = await self.select_tg_profile_by_tg_id(tg_id)
        return tg_profile.nickname

    async def update_nickname(self, tg_id: int, new_nickname: str) -> bool:
        """
        The method change  nickname from tg_profile
        @param tg_id: User ID from telegram
        @param new_nickname: new nickname
        @return: true if success else false
        """
        tg_profile = await self.select_tg_profile_by_tg_id(tg_id)
        if not tg_profile:
            return False
        await tg_profile.update(nickname=new_nickname).apply()
        return True

    @staticmethod
    async def select_all_requests_user(user_id) -> List[RideRequest]:
        """
        The method selection of all user ride_requests
        @param user_id: User ID
        @return: list of all user ride requests
        """
        all_requests_user = await RideRequest.query.where(RideRequest.author == user_id).gino.all()
        return all_requests_user

    @staticmethod
    async def check_user_in_database(user_id: int) -> bool:
        """
        The method checks if the user exists in the database
        @param user_id: User ID
        @return: true if user in database else false
        """
        user = await User.query.where(User.id == user_id).gino.first()
        return bool(user)

    @staticmethod
    async def select_all_tg_profile() -> List[TgProfile]:
        """
        The method selects all records from the tg_profiles table
        @return:list of tg_profile objects
        """
        tg_profiles = await TgProfile.query.gino.all()
        return tg_profiles
