"""
    The file contains commands for working with the database
"""
# эту строку использовать если запускаете весь проект
from src.packages.database.shemas import User, Request, db
# эту строку использовать если запускаете database.test
# from shemas import User, Request, db
from asyncpg import UniqueViolationError


async def add_user(tg_nik, tg_id, first_name, last_name, car_brend, car_model,
                   car_number, phone_number):
    '''
    Function to add a record to a table users
    :param tg_nik: nickname from telegram
    :param tg_id: id from telegram
    :param first_name: first_name from telegram
    :param last_name: last_name from telegram
    :param car_brend: car brand entered by the user
    :param car_model: car model entered by the user
    :param car_number: car number entered by the user
    :param phone_number: phone number entered by the user
    :return:nothing
    '''
    try:
        user = User(tg_nik=tg_nik, tg_id=tg_id, first_name=first_name,
                    last_name=last_name, car_brend=car_brend,
                    car_model=car_model, car_number=car_number,
                    phone_number=phone_number)
        await user.create()
        print("Пользователь добавлен")
    except UniqueViolationError:
        print("Пользователь не добавлен")


async def select_all_users():
    """
    The function selects all records from the users table
    :return:list of user objects
    """
    users = await User.query.gino.all()
    return users


async def count_users():
    """
    The function to count the number of users in the users table
    :return: count users
    """
    count = await db.func.count(User.id).gino.scalar()
    return count


async def select_user(id):
    """
    The function selection user by id from the table
    :param id: User ID
    :return: user object from users table
    """
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_user_tg_id(tg_id):
    """
    The function selection user by telegram_id from the table
    :param tg_id: User ID from telegram
    :return: user object from users table
    """
    user = await User.query.where(User.tg_id == tg_id).gino.first()
    return user


async def add_request(date, time, terms_delivery, place_departure,
                      place_comming, number_of_seats, driver):
    '''
    Function to add a record to a table requests
    :param date: date entered by the user
    :param time: time entered by the user
    :param terms_delivery: terms_delivery entered by the user
    :param place_departure: place_departure entered by the user
    :param place_comming: place_comming entered by the user
    :param number_of_seats: number_of_seats entered by the user
    :param driver: user id from users table
    :return:nothing
    '''
    try:
        new_request = Request(date=date, time=time,
                              terms_delivery=terms_delivery,
                              place_departure=place_departure,
                              place_comming=place_comming,
                              number_of_seats=number_of_seats, driver=driver)
        await new_request.create()
    except UniqueViolationError:
        print("Заявка не добавлена")


async def select_all_request():
    """
     The function selects all records from the requests table
     :return:list of requests objects
     """
    requests_all = await Request.query.gino.all()
    return requests_all


async def count_request():
    """
    The function to count the number of request in the requests table
    :return: count requests
    """
    count = await db.func.count(Request.id).gino.scalar()
    return count


async def select_all_requests_user(user_id):
    """
    The function selection of all user requests
    :param id: User ID
    :return: list all user requests
    """
    all_requests_user = await Request.query.where(Request.driver == user_id).gino.all()
    return all_requests_user
