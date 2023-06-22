from typing import Optional
from contextlib import contextmanager
from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from model.alchemy.install import sqlite_engine


class AbstractSessionProvider(ABC):
    """
    Abstract class of session provider.
    provider should implement the following methods:
        create_session: creates and returns
            SQLAlchemy session (preferrably scoped, will
            be used in a separate tread)
        close: close session
        error: rollback session on error
    """

    @abstractmethod
    def create_session(self) -> Session: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def error(self) -> None: ...

    @contextmanager
    def __call__(self, *args, **kwargs):
        try:
            yield self.create_session()
        except Exception as e:
            self.error()
        finally:
            self.close()


class OneTimeSessionProvider(AbstractSessionProvider):
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

    def create_session(self) -> Session:
        self.__engine = sqlite_engine(self.__file_name)
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
