"""
Initialization file for the packages database, schemas.
"""
from .database import *
from .tables import *

# pylint:disable=E0603
__all__ = [
    "database",
    "setup_database",
    "DatabaseException",
    "UserTable",
    "TelegramProfileTable",
    "CarTable",
    "RideRequestTable",
]

database = Database()


# pylint:disable=W0621, C0103, C0116
async def setup_database(db: database):
    await db.connect_db()
    await db.create_tables()
