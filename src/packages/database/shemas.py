"""
    The file to create database tables
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Time, sql, ForeignKey
from sqlalchemy.orm import relationship
from gino import Gino

db = Gino()


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
    car_id = Column(Integer(), primary_key=True)
    model = Column(String(30), nullable=False)
    brand = Column(String(30), nullable=False)
    number_plate = Column(String(9), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="cascade", onupdate="cascade"))
    query: sql.select


class TgProfile(BaseModel):
    """
    The class to create tg_profile table
    """

    __tablename__ = "tg_profiles"
    tg_id = Column(BigInteger(), primary_key=True, autoincrement=False)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="cascade", onupdate="cascade"))
    nickname = Column(String(50), nullable=False)
    query: sql.select


class User(BaseModel):
    """
    The class to create users table
    """

    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    tg_id = Column(BigInteger(), nullable=False, unique=True)
    car_id = Column(Integer())
    telegram_profile = relationship("TgProfile", cascade="all,delete,delete-orphan", passive_deletes=True)
    car = relationship("Car", cascade="all,delete,delete-orphan", passive_deletes=True)
    query: sql.select


class RideRequest(db.Model):
    """
    The class to create ride requests table
    """

    __tablename__ = "ride_requests"
    id = Column(Integer(), primary_key=True)
    author = Column(Integer(), ForeignKey("users.id", ondelete="cascade"), nullable=False)
    delivery_terms = Column(String())
    date = Column(Date(), nullable=False)
    time = Column(Time(), nullable=False)
    departure_place = Column(String, nullable=False)
    destination_place = Column(String, nullable=False)
    seats_number = Column(Integer, nullable=False)
    post_message_id = Column(Integer, nullable=False)
    query: sql.select
