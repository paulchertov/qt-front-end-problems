from typing import Callable

from PySide6.QtCore import QObject, Signal

from model.alchemy.session import AbstractSessionProvider
from tasks.db import PSTask, PSDBTask


class PSService(QObject):
    """
    Base class for services
    """


class PSDbService(PSService):
    """
    Base class for services that work with database

    Fields:
        session_provider: AbstractSessionProvider - provider for database session
    """
    def __init__(self, session_provider: AbstractSessionProvider):
        super().__init__()
        self.session_provider = session_provider
