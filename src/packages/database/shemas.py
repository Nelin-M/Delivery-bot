"""
    The file to create database tables
"""

from sqlalchemy import Table, Column, Integer, String, Date, Time, sql, inspect, \
    ForeignKey
from typing import List
from gino import Gino

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True


class User(BaseModel):
    """
        The class to create users table
    """
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    tg_nik = Column(String(), unique=True)
    tg_id = Column(Integer(), nullable=False, unique=True)
    first_name = Column(String())
    last_name = Column(String())
    car_brend = Column(String())
    car_model = Column(String())
    car_number = Column(String())
    phone_number = Column(String())
    query: sql.select


class Request(db.Model):
    """
        The class to create requests table
    """
    __tablename__ = 'requests'
    id = Column(Integer(), primary_key=True)
    driver = Column(Integer(), ForeignKey('users.id'), nullable=False)
    terms_delivery = Column(String)
    date = Column(Date(), nullable=False)
    time = Column(Time(), nullable=False)
    place_departure = Column(String, nullable=False)
    place_comming = Column(String, nullable=False)
    number_of_seats = Column(Integer, nullable=False)
    query: sql.select
