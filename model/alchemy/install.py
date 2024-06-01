"""
This module is used to install the tables in the database.

Functions:
    sqlite_engine: Create a sqlite engine
    install: Create tables in the database
"""

from sqlalchemy import create_engine

from model.alchemy.tables import *


def sqlite_engine(file_name: str):
    return create_engine(
        f'sqlite:///{file_name}',
        echo=1
    )


def install(engine):
    Base.metadata.create_all(engine)
