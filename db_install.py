from random import randint, choice
from sqlalchemy import create_engine

from model.alchemy.tables import *


engine = create_engine(
    f'sqlite:///db.db',
    echo=1
)

Base.metadata.create_all(engine)