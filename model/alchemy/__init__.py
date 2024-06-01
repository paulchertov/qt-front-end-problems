"""
Module for SQLAlchemy ORM related things'

Modules:
    session: Session provider for SQLAlchemy, used in Qt application
    tables: Tables for the database
    install: Set Up of the database
Items:
    Base: Base class for SQLAlchemy models
"""


from sqlalchemy.orm import declarative_base


Base = declarative_base()


