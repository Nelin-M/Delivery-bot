"""
    The file contains commands for working with the database
"""
from src.packages.database.shemas import User, RideRequest, Car, TgProfile, db
from sqlalchemy import sql
from asyncpg import UniqueViolationError
from datetime import date
from datetime import time

__all__ = ["Database"]


class Database():
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    async def connect_db(self):
        await db.set_bind(
            f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}')

    async def drop_tables(self):
        await db.gino.drop_all()

    async def create_tables(self):
        await db.gino.create_all()

    async def add_user(self, tg_id: int, first_name: str, last_name: str,
                       car_id: int, phone_number: str):
        '''
        The method to add a record to a table users
        @param tg_id: id from telegram
        @param first_name: first_name from telegram
        @param last_name: last_name from telegram
        @param car_id: car_id from cars table
        @param phone_number: phone number entered by the user
        @return:nothing
        '''
        try:
            user = User(tg_id=tg_id, first_name=first_name, last_name=last_name,
                        car_id=car_id, phone_number=phone_number)
            await user.create()
            print("Пользователь добавлен")
        except UniqueViolationError:
            print("Пользователь не добавлен")

    async def add_tg_profile(self, tg_id: int, nickname: str):
        """
        The method adding a record to  table tg_profiles
        @param tg_id: id from telegram
        @param nickname: nickname from telegram
        @return:nothing
        """
        try:
            tg_profile = TgProfile(tg_id=tg_id, nickname=nickname)
            await tg_profile.create()
            print("Запись в таблицу tg_profiles добавлена")
        except UniqueViolationError:
            print("Запись в таблицу tg_profiles не добавлена")

    async def add_car(self, model: str, brand: str, number_plate: str):
        """
        The method adding a record to table cars
        @param model: the model of car
        @param brand: the brand of car
        @param number_plate: the number_plate of car
        @return: id of the car added to the table
        """
        try:
            car = Car(model=model, brand=brand, number_plate=number_plate)
            car = await car.create()
            print("Запись в таблицу cars добавлена")
            return car.id
        except UniqueViolationError:
            print("Запись в таблицу cars не добавлена")

    async def add_request(self, author: int, delivery_terms: str, date: date,
                          time: time, departure_place: str,
                          destination_place: str, seats_number: int):
        """
        The method adding a record to  table ride_requests
        @param author: user id from users table
        @param delivery_terms:delivery_terms
        @param date:date
        @param time:time
        @param departure_place:departure_place
        @param destination_place:destination_place
        @param seats_number: number of seats places
        @return:nothing
        """
        try:
            new_request = RideRequest(author=author,
                                      delivery_terms=delivery_terms, date=date,
                                      time=time,
                                      departure_place=departure_place,
                                      destination_place=destination_place,
                                      seats_number=seats_number)
            await new_request.create()
        except UniqueViolationError:
            print("Заявка не добавлена")

    async def select_all_requests(self):
        """
         The method selects all records from the ride_requests table
         @return:list of ride_requests objects
         """
        ride_requests_all = await RideRequest.query.gino.all()
        return ride_requests_all

    async def select_all_users(self):
        """
        The method selects all records from the users table
        @return:list of user objects
        """
        users = await User.query.gino.all()
        return users

    async def select_all_cars(self):
        """
        The method selects all records from the cars table
        @return:list of car objects
        """
        cars = await Car.query.gino.all()
        return cars

    async def count_users(self):
        """
        The method to count the number of users in the users table
        @return: count users
        """
        count = await db.func.count(User.id).gino.scalar()
        return count

    async def count_ride_requests(self):
        """
        The method to count the number of ride_request in the ride_request table
        @return: count ride_requests
        """
        count = await db.func.count(RideRequest.id).gino.scalar()
        return count

    async def count_cars(self):
        """
        The method to count the number of car in the cars table
        @return: count cars
        """
        count = await db.func.count(Car.tg_id).gino.scalar()
        return count

    async def count_tg_profiles(self):
        """
        The method to count the number of tg_profile in the tg_profiles table
        @return: count tg_profiles
        """
        count = await db.func.count(TgProfile.tg_id).gino.scalar()
        return count

    async def select_user(self, id: int):
        """
        The method selection user by id from the table
        @param id: User ID
        @return: user object from users table
        """
        user = await User.query.where(User.id == id).gino.first()
        return user

    async def select_user_by_tg_id(self, tg_id: int):
        """
        The method selection user by telegram_id from the table
        @param tg_id: User ID from telegram
        @return: user object from users table
        """
        user = await User.query.where(User.tg_id == tg_id).gino.first()
        return user

    async def select_car_by_id(self, id: int):
        """
        The method selection car by id from the table cars
        @param id: car id
        @return: car object from cars table
        """
        car = await Car.query.where(Car.id == id).gino.first()
        return car

    async def select_tg_profile_by_tg_id(self, tg_id: int):
        """
        The method selection tg_profile by tg_id from the table tg_profiles
        @param tg_id: User ID from telegram
        @return: tg_profile object from tg_profiles table
        """
        tg_profile = await TgProfile.query.where(
            TgProfile.tg_id == tg_id).gino.first()
        return tg_profile

    async def select_nickname_from_tg_profile_by_tg_id(self, tg_id: int):
        """
        The method selection nickname from tg_profile by tg_id from the table tg_profiles
        @param tg_id: User ID from telegram
        @return: nickname
        """
        tg_profile = await TgProfile.query.where(
            TgProfile.tg_id == tg_id).gino.first()
        return tg_profile.nickname

    async def update_nickname(self, tg_id: int, new_nickname: str):
        """
         The method change  nickname from tg_profile
         @param tg_id: User ID from telegram
         @param new_nickname: new nickname
         @return:nothing
         """
        tg_profile = await TgProfile.query.where(
            TgProfile.tg_id == tg_id).gino.first()
        await tg_profile.update(nickname=new_nickname).apply()

    async def select_all_requests_user(self, user_id):
        """
        The method selection of all user ride_requests
        @param id: User ID
        @return: list all user ride_requests
        """
        all_requests_user = await RideRequest.query.where(
            RideRequest.author == user_id).gino.all()
        return all_requests_user

    async def check_user_in_database(self, user_id: int):
        """
        The method checks if the user exists in the database
        @param user_id: User ID
        @return: bool
        """
        users = await User.query.where(User.id == user_id).gino.first()
        return True if users is not None else False

    async def select_all_tg_profile(self):
        """
        The method selects all records from the tg_profiles table
        @return:list of tg_profile objects
        """
        tg_profiles = await TgProfile.query.gino.all()
        return tg_profiles
