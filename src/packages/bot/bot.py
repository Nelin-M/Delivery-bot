"""
This module contains Bot functions associated with answers.
"""
from src.packages.logger import Log, Loggers

__all__ = ["Bot"]


class BotException(Exception):
    """
    Class-exception for any errors with bot working.
    """


class Bot:
    """
    A chat-bot class with the functionality necessary to generate a response to a user's message.
    """

    __logger = None

    def __init__(self, logger: Log) -> None:
        """
        Initialize Bot class with logger.
        @param logger: custom class responsible for logging.
        """
        self.__logger = logger

    def generate_answer(self, text: str) -> str:
        """
        @param text: some message from user.
        @return: return user text.
        """
        self.__log_message(text)
        return text

    def __log_message(self, text: str) -> None:
        """
        Logging user message.
        @param text: some question from user.
        """
        self.__logger.info(Loggers.INCOMING.value, f'"{text}";')
