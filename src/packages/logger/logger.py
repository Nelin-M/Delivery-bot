"""
A module with the implementation of the main methods for logging.
"""
import enum
import logging
from src.packages.loaders import config

__all__ = ["Log", "Loggers"]


class LoggerException(Exception):
    """
    Exception class for the logger.
    """


class Loggers(enum.Enum):
    """
    Enumeration of available loggers in the application.
    """

    APP = "app"
    INCOMING = "incoming"


def _init_file_handler(logger_name: str) -> logging.FileHandler:
    """
    Initializing file handler from the __logging__ library with the required parameters.
    @param logger_name: a string with the name of the logger for which the logger needs to be initialized.
    @return: A handler class from the __logging__ library which writes formatted logging records to disk files.
    """
    file_handler = logging.FileHandler(config["log_filename"], encoding=config["log_encoding"])
    file_handler.setFormatter(
        logging.Formatter(
            config["logging_formats"][logger_name],
            datefmt=config["logging_date_format"],
        )
    )
    return file_handler


class Log:
    """
    Logger class. An object of this class writes logs to a file with five logging severity.
    The logger class has two types of loggers, the first _app_ for logging the application state,
    the second _incoming_ for logging received messages.
    """

    _loggers = {}

    def __init__(self) -> None:
        """
        Constructor for objects.
        """
        self._loggers = {}
        self.__init_loggers()
        self.__add_file_handlers_to_loggers()

    def __init_loggers(self) -> None:
        """
        Initialization of two loggers - _app_ for the application and _incoming_ for incoming messages.
        """
        self._loggers[Loggers.APP.value] = logging.getLogger(Loggers.APP.value)
        self._loggers[Loggers.APP.value].setLevel(logging.INFO)

        self._loggers[Loggers.INCOMING.value] = logging.getLogger(Loggers.INCOMING.value)
        self._loggers[Loggers.INCOMING.value].setLevel(logging.INFO)

    def __add_file_handlers_to_loggers(self) -> None:
        """
        Adding a file handler from the __logging__ library for all loggers.
        """
        for logger_name in list(self._loggers.keys()):
            file_handler = _init_file_handler(logger_name)
            self._loggers[logger_name].addHandler(file_handler)

    def __check_logger_name_for_existence(self, logger_name: str) -> None:
        """
        Checking for existence of a logger named `logger_name`.
        @param logger_name: the name of the logger that needs to be checked for existence.
        @raise LoggerException: if no logger with the same name exists.
        """
        if logger_name not in self._loggers.keys():
            raise LoggerException(f"No such logger: {logger_name}.")

    def info(self, logger_name: str, message: str) -> None:
        """
        Logging a message with the severity of _info_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self._loggers[logger_name].info(message)
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def info_from_handlers(
        self, logger_name: str, tg_id: int, name_func: str, message_from_user: str, text_info=""
    ) -> None:
        """
        Logging a message with the severity of _info_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self.info(logger_name, f"tg_id={tg_id},func={name_func}, mess={message_from_user},info={text_info}")
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def debug(self, logger_name: str, message: str) -> None:
        """
        Logging a message with the severity of _debug_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self._loggers[logger_name].debug(message)
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def debug_from_handlers(
        self, logger_name: str, tg_id: int, name_func: str, message_from_user: str, text_info: str
    ) -> None:
        """
        Logging a message with the severity of _debug_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self.debug(
                logger_name, f"Пользователь tg_id={tg_id},func={name_func}, mess={message_from_user},info={text_info}"
            )
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def warning(self, logger_name: str, message: str) -> None:
        """
        Logging a message with the severity of _warning_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self._loggers[logger_name].warning(message)
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def warning_from_handlers(
        self, logger_name: str, tg_id: int, name_func: str, message_from_user: str, text_info: str
    ) -> None:
        """
        Logging a message with the severity of _warning_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        try:
            self.warning(
                logger_name, f"Пользователь tg_id={tg_id},func={name_func}, mess={message_from_user},info={text_info} "
            )
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def error(self, logger_name: str, message: str) -> None:
        """
        Logging a message with the severity of _error_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self._loggers[logger_name].error(message)
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def error_from_handlers(
        self, logger_name: str, tg_id: int, name_func: str, message_from_user: str, text_info: str
    ) -> None:
        """
        Logging a message with the severity of _error_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self.error(
                logger_name, f"Пользователь tg_id={tg_id},func={name_func}, mess={message_from_user},info={text_info}"
            )
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def critical(self, logger_name: str, message: str) -> None:
        """
        Logging a message with the severity of _critical_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self._loggers[logger_name].critical(message)
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception

    def critical_from_handlers(
        self, logger_name: str, tg_id: int, name_func: str, message_from_user: str, text_info: str
    ) -> None:
        """
        Logging a message with the severity of _critical_.
        @param logger_name: the name of the logger that should write the log.
        @param message: the text of the message that is written to the log.
        @raise LoggerException: if unexpected error.
        """
        self.__check_logger_name_for_existence(logger_name)
        try:
            self.critical(
                logger_name, f"Пользователь tg_id={tg_id},func={name_func}, mess={message_from_user},info={text_info}"
            )
        except Exception as exception:
            raise LoggerException(f"Unexpected error: {exception}.") from exception
