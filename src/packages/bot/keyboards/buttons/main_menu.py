"""
Keyboard for the main menu
"""
from src.packages.bot.keyboards.UtilsButtons import ReplyResizeKeyboardAndOneTimeList

main_menu_authorised = ReplyResizeKeyboardAndOneTimeList(["Создать заявку", "Такси", "Мои заявки",
                                                          "Мой автомобиль", "Обратная связь", "Пожаловаться",
                                                          "Назад"], 3)

main_menu_unauthorised = ReplyResizeKeyboardAndOneTimeList(["Создать профиль"], 3)
