"""
    The file to create database tables
"""

from sqlalchemy import Column, Integer, String, Date, Time, sql, ForeignKey
from gino import Gino

db = Gino()


# pylint: disable=C0115
class BaseModel(db.Model):
    """
    The class of Base Model
    """

    __abstract__ = True


class Car(BaseModel):
    """
    The class to create car table
    """

    __tablename__ = "cars"
    id = Column(Integer(), primary_key=True)
    model = Column(String(30), nullable=False)
    brand = Column(String(30), nullable=False)
    number_plate = Column(String(9), nullable=False)
    query: sql.select


class TgProfile(BaseModel):
    """
    The class to create tg_profile table
    """

    __tablename__ = "tg_profiles"
    tg_id = Column(Integer(), primary_key=True, autoincrement=False)
    nickname = Column(String(50), nullable=False)
    query: sql.select


class User(BaseModel):
    """
    The class to create users table
    """

    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    tg_id = Column(Integer(), ForeignKey("tg_profiles.tg_id"), nullable=False, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    car_id = Column(Integer(), ForeignKey("cars.id"))
    phone_number = Column(String(10))
    query: sql.select


class RideRequest(db.Model):
    """
    The class to create ride requests table
    """

    __tablename__ = "ride_requests"
    id = Column(Integer(), primary_key=True)
    author = Column(Integer(), ForeignKey("users.id"), nullable=False)
    delivery_terms = Column(String())
    date = Column(Date(), nullable=False)
    time = Column(Time(), nullable=False)
    departure_place = Column(String, nullable=False)
    destination_place = Column(String, nullable=False)
    seats_number = Column(Integer, nullable=False)
    query: sql.select
