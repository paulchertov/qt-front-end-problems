from sqlalchemy import create_engine

from model.alchemy.tables import *


def sqlite_engine(file_name: str):
    return create_engine(
        f'sqlite:///{file_name}',
        echo=1
    )


def install(engine):
    Base.metadata.create_all(engine)
