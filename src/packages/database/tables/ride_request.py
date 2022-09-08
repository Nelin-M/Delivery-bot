"""
Module keeps methods to operate with database ride request table
"""
from typing import List
from datetime import date, time
from asyncpg import UniqueViolationError
from src.packages.database.shemas import RideRequest
from ..database import DatabaseException


# pylint: disable=R0904:
class RideRequestTable:
    """
    This class is to operate with database ride request table
    """

    # pylint:disable=R0913
    @staticmethod
    async def add(
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
    async def get_single_ride_request(ride_request_id: int) -> RideRequest:
        """
        This method returns a single RideRequest object
        @param ride_request_id: RideRequest.id
        @return: RideRequest
        """
        ride_request = await RideRequest.query.where(RideRequest.id == ride_request_id).gino.first()
        return ride_request

    @staticmethod
    async def get_user_ride_requests(user_id) -> List[RideRequest]:
        """
        This method returns list of user ride requests
        @param user_id: User ID
        @return: list with RideRequest objects
        """
        user_ride_requests = await RideRequest.query.where(RideRequest.author == user_id).gino.all()
        return user_ride_requests

    @classmethod
    async def update(cls, ride_request_id: int, **data):
        """
        This method updates RideRequest object
        @param ride_request_id:
        @param data: data to update
        @return:
        """
        # try:
        ride_request = await cls.get_single_ride_request(ride_request_id)
        await ride_request.update(**data).apply()
        # except:
        #     pass

    @classmethod
    async def delete(cls, ride_request_id: int):
        """
        This method deletes RideRequest object
        @param ride_request_id:
        @return:
        """
        # try:
        ride_request = await cls.get_single_ride_request(ride_request_id)
        await ride_request.delete()
        # except:
        #     pass
