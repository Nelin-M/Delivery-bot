"""
This module represents car profile ReplyKeyboards
"""
from src.packages.bot.keyboards.UtilsButtons import ReplyResizeKeyboardAndOneTimeList

add_car_menu = ReplyResizeKeyboardAndOneTimeList(["Добавить автомобиль"])

car_added_menu = ReplyResizeKeyboardAndOneTimeList(["Редактировать автомобиль", "Удалить автомобиль"],
                                                   cancel_button=True)

car_create_confirmation_keyboard = ReplyResizeKeyboardAndOneTimeList(["Всё верно", "Хочу исправить"],
                                                                     cancel_button=True)

car_delete_confirmation = ReplyResizeKeyboardAndOneTimeList(["Да", "Отменить"])

car_edit_cancel = ReplyResizeKeyboardAndOneTimeList(["Отмена"])

car_create_confirmation_keyboard = ReplyResizeKeyboardAndOneTimeList(["Всё верно", "Хочу исправить"],
                                                                     cancel_button=True)

car_delete_confirmation = ReplyResizeKeyboardAndOneTimeList(["Да", "Отменить"])
