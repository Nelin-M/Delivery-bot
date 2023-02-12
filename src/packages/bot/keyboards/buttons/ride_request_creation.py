"""
This module represents ride request creation ReplyKeyboards
"""

import emoji

from src.packages.bot.keyboards.UtilsButtons import ReplyResizeKeyboardList

keyboard_ok = ReplyResizeKeyboardList(["Отправить", "Редактировать",
                                       "Отменить заявку"])

keyboard_main_profile = ReplyResizeKeyboardList(["Мой автомобиль"])

keyboard_terms_delivery = ReplyResizeKeyboardList(["Дальше",
                                                   "За шоколадку " + emoji.emojize(":chocolate_bar:")],
                                                  1, cancel_button=True)

keyboard_place_departure = ReplyResizeKeyboardList(["ул.Звездова 101 A"],
                                                   1, cancel_button=True)

default_keyboard = ReplyResizeKeyboardList(["Отмена"])

number_of_seats_keyboard = ReplyResizeKeyboardList([str(i) for i in range(1, 5)],
                                                   cancel_button=True)

time_keyboard = ReplyResizeKeyboardList(["23:15", "00:45", "01:15",
                                         "02:15", "07:15", "08:15"],
                                        3, cancel_button=True)

yes_no_keyboard = ReplyResizeKeyboardList(["Да", "Не прикреплять ссылку",
                                           "Изменить адрес"])
