"""
This module is responsible for loading the configuration file for the bot and loading the environment variables.
"""
import json
from typing import Dict, Optional, Union
from dotenv import dotenv_values, find_dotenv
from packages.path_storage import PathStorage

__all__ = ["ConfigLoader"]


class ConfigException(Exception):
    """
    Class-exception for any errors with config loading.
    """


class ConfigLoader:
    """
    Class ConfigLoader responding for loading config loading api key for telegram.
    """

    _CONFIG_FILE_PATH = PathStorage.get_path_to_setting() / "bot_config.json"
    _CONFIG_FILE_ENCODING = "utf-8"
    _CONFIG_FILE_READ_MODE = "r"

    @classmethod
    def load_config(cls) -> Dict[str, Union[float, str, dict, list]]:
        """
        Loading config file.
        @return: bot config json file.
        @raise ConfigException: if config file doesn't exists.
        """
        try:
            with open(
                cls._CONFIG_FILE_PATH,
                cls._CONFIG_FILE_READ_MODE,
                encoding=cls._CONFIG_FILE_ENCODING,
            ) as config_file:
                _config = json.load(config_file)
                return _config
        except FileNotFoundError as exception:
            raise ConfigException(f"Can't find bot config file: {exception}") from exception

    @classmethod
    def load_env_variables(cls) -> Dict[str, Optional[str]]:
        """
        Loading environment variables from a .env file and returns them as a dictionary.
        @return: dict with environment variables.
        @raise ConfigException: if `.env` file not found.
        """
        try:
            return dotenv_values(find_dotenv(raise_error_if_not_found=True))
        except IOError as exception:
            raise ConfigException(f"Can't find .env file: {exception}") from exception
