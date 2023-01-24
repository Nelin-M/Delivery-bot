"""
Module to keep texts used in bot answers
"""
from src.packages.loaders import env_variables

channel_link = env_variables.get("CHANNEL_LINK")
# todo: реализовать модуль для выдачи текстов, с указанием разметки,
#  проверкой на корректность разметки и экранировкой символов, например, символов в ссылках
MAIN_MENU_AUTHORISED = (
    f"Созданные внутри бота заявки публикуются в [данном]({channel_link}) телеграм канале.\n\n"
    f"[Инструкция по созданию заявки]"
    f"({'https://telegra.ph/Instrukciyu-po-ispolzovaniyu-servisa-DeliveryBot-09-06'})\n\n"
    f"Продолжая пользоваться сервисом вы подтверждаете ваше согласие с "
    f"[{'правилами'}]({'https://telegra.ph/Pravila-ispolzovaniya-servisa-DeliveryBot-09-06'})!\n\n"
    f"Для возможности создавать заявки, просим вас добавить данные автомобиля, для этого "
    f"в нижнем меню, нажмите кнопку «Мой автомобиль» и заполните все необходимые поля"
)

MAIN_MENU_UNAUTHORISED = """Добро пожаловать в наш сервис.
Для удобства дальнейшего использования
и возможности создавать заявки,
просим вас создать профиль,
для этого нажмите кнопку «Создать профиль»"""
