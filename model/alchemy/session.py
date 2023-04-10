from typing import Protocol, Optional, Generator
from contextlib import ContextDecorator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session


class ISessionProvider(Protocol):
    """
    Interface of session provider.
    provider should implement the following methods:
        session: creates and returns SQLAlchemy session (preferrably scoped, will be used
            in a separate tread
        close: close session
        error: rollback session on error
    """
    def session(self) -> Session: ...
    def close(self) -> None: ...
    def error(self) -> None: ...


class OneTimeSessionProvider:
    """
    Barbaric way to create and drop all machinery around session
    on each request
    """
    def __init__(self, file_name: str, debug: Optional[bool] = False):
        self.__connection: Optional[Connection] = None
        self.__session: Optional[Session] = None
        self.__engine: Optional[Engine] = None
        self.__file_name = file_name
        self.__debug = debug

    def session(self) -> Session:
        self.__engine = create_engine(
            f'sqlite:///{self.__file_name}',
            echo=self.__debug,
            convert_unicode=True
        )
        self.__connection = self.__engine.connect()
        self.__session = scoped_session(
            sessionmaker(autocommit=False, autoflush=True, bind=self.__engine)
        )
        return self.__session

    def close(self) -> None:
        if self.__session is not None:
            self.__session.close()
        if self.__connection is not None:
            self.__connection.close()
        if self.__engine:
            self.__engine.dispose()

    def error(self) -> None:
        if self.__session is not None:
            self.__session.rollback()
