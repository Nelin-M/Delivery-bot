"""
    The file for database testing
"""
import asyncio
from shemas import db
from commands import add_user, select_all_users, select_user, count_users, \
    count_request, select_all_requests_user
from src.packages.loaders import env_variables

host = env_variables.get("HOST")
user = env_variables.get("USER")
password = env_variables.get("PASSWORD")
db_name = env_variables.get("DB_NAME")
# данные для сохранения аользователей в бд
values = {"tg_nik": "dssss", "tg_id": 900, "first_name": '', "last_name": "",
          "car_brend": "", "car_model": "", "car_number": "",
          "phone_number": ""}

values1 = {"tg_nik": "dasha", "tg_id": 9000, "first_name": '', "last_name": "",
           "car_brend": "", "car_model": "", "car_number": "",
           "phone_number": ""}


async def main():
    # подключение к базе данных
    await db.set_bind(
        f'postgresql+asyncpg://{user}:{password}@{host}/{db_name}')
    # удаление всех таблиц
    # await db.gino.drop_all()
    # создание всех таблиц
    # await db.gino.create_all()
    # добавление пользователей
    await add_user(**values)
    await add_user(**values1)
    # выбор всех пользователей
    users = await select_all_users()
    print((users[1]).id)
    # выбор пользователя по id
    select_user_id_1 = await select_user(1)
    print(select_user_id_1.id)
    # кол-во всех пользователей
    count = await count_users()
    print(count)
    # кол-во всех заявок
    count_1 = await count_request()
    print("Кол-во заявок", count_1)
    #  все заявки пользователя по его id
    all_requests_user = await select_all_requests_user(3)
    for i in all_requests_user:
        print(i.terms_delivery)


# запуск функции main() асинхронно
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
