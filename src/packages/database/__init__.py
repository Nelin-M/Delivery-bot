"""
Initialization file for the packages database, schemas.
"""
from .database import *

__all__ = ["database", "setup_database"]

database = Database()


# pylint:disable=W0621, C0103, C0116
async def setup_database(db: database):
    await db.connect_db()
