"""
Module keeps methods to operate with database car table
"""
from asyncpg import UniqueViolationError
from src.packages.database.shemas import Car
from ..database import DatabaseException


class CarTable:
    """
    This class is to operate with database car table
    """

    @staticmethod
    async def add(model: str, brand: str, number_plate: str, user_id: int) -> int:
        """
        The method adding a record to table cars
        @param model: the model of car
        @param brand: the brand of car
        @param number_plate: the number_plate of car
        @param user_id: id from tables users
        @return: id of the car added to the table cars
        """
        try:
            car = Car(model=model, brand=brand, number_plate=number_plate, user_id=user_id)
            car = await car.create()
            return car.car_id
        except UniqueViolationError as exception:
            raise DatabaseException("Автомобиль уже существует в базе данных.") from exception

    @staticmethod
    async def get(car_id: int) -> Car:
        """
        The method selection car by id from the table cars
        @param car_id: car id
        @return: car object from cars table
        """
        car = await Car.query.where(Car.car_id == car_id).gino.first()
        return car

    @staticmethod
    async def get_by_user_id(user_id: int) -> Car:
        """
        The method selection car by id from the table cars
        @param user_id: id from tables users
        @return: car object from cars table
        """
        car = await Car.query.where(Car.user_id == user_id).gino.first()
        return car

    @classmethod
    async def update(cls, car_id: int, data: dict):
        """
        This method updates Car object
        @param car_id: Car.id
        @param data: data to update
        @return:
        """
        # try:
        car = await cls.get(car_id)
        await car.update(**data).apply()
        # except:
        #     pass

    @classmethod
    async def delete(cls, car_id: int):
        """
        This method deletes Car object
        @param car_id: Car.id
        @return:
        """
        # try:
        car = await cls.get(car_id)
        await car.delete()
        # except:
        #     pass
