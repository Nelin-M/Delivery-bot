"""
Initialization file for the packages database, shemas.
"""
from .database import *


database = Database()


# pylint:disable=W0621, C0103, C0116
async def setup_database(db: database):
    await db.connect_db()
    await db.create_tables()


__all__ = ["database", "setup_database"]
