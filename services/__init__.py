from typing import Callable

from PySide6.QtCore import QObject, Signal

from model.alchemy.session import AbstractSessionProvider
from tasks.db import PSTask, PSDBTask


class PSService(QObject):
    def __init__(self, session_provider: AbstractSessionProvider):
        super().__init__()
        self.session_provider = session_provider
