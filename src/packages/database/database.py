"""
The file contains commands for working with the database
"""
from src.packages.database.shemas import db
from src.packages.logger import Loggers, logger
from src.packages.loaders import env_variables

__all__ = ["Database", "DatabaseException"]


class DatabaseException(Exception):
    """
    Class-exception for any errors with database working.
    """


# pylint: disable=R0904:
class Database:
    """
    Database class.The class contains the necessary
    methods for working with the postgres sql database.
    """

    def __init__(self):
        self.user = env_variables.get("POSTGRES_USER")
        self.password = env_variables.get("POSTGRES_PASSWORD")
        self.host = env_variables.get("POSTGRES_HOST")
        self.port = env_variables.get("POSTGRES_PORT", 5432)
        self.db_name = env_variables.get("POSTGRES_DB")

    async def connect_db(self):
        """
        method to connect to postgres database
        """
        try:
            await db.set_bind(
                f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            )
        # pylint: disable=W0703:
        except Exception as exception:
            logger.critical(Loggers.APP.value, f"Unexpected error: {exception}")
            raise exception

    @staticmethod
    # pylint: disable=W0238:
    async def __drop_tables():
        await db.gino.drop_all()

    @staticmethod
    # pylint: disable=W0238:
    async def __create_tables():
        await db.gino.create_all()
