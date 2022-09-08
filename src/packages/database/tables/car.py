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
    async def add(model: str, brand: str, number_plate: str) -> int:
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
    async def get(car_id: int) -> Car:
        """
        The method selection car by id from the table cars
        @param car_id: car id
        @return: car object from cars table
        """
        car = await Car.query.where(Car.id == car_id).gino.first()
        return car

    @classmethod
    async def update(cls, car_id: int, **data):
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
