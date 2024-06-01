"""
"""
from typing import Any

from PySide6.QtCore import Signal
from sqlalchemy.orm.session import Session

from tasks import PSTask
from model.alchemy.session import AbstractSessionProvider


class PSDBTask(PSTask):
    """
    Abstract class for DB task, subclass must implement query method
    signals: error_occurred(Exception) - emits Exception that occurred
    should implement the following methods:
        success: return success signal, signal should also be created
            as a class attribute
        query: db operations to be done, they should return value
            or transport item or list of transport items, returned tuple
            will be passed as separate arguments sequentially

    methods:
        run: run QThread, this method should not be overridden
    """
    def __init__(
        self,
        id: str,
        session_provider: AbstractSessionProvider
    ):
        super().__init__(id)
        self.session_provider = session_provider

    def __del__(self):
        self.session_provider.close()

    def success(self) -> Signal:
        raise NotImplementedError("Successful signal was not set for the class")

    def query(self, session: Session) -> Any:
        raise NotImplementedError("Query method was not implemented")

    def run(self):
        result = None
        error = None
        with self.session_provider() as session:
            try:
                result = self.query(session)
            except Exception as e:
                error = e
                raise e

        if error is not None:
            self.error_occurred.emit(error)
        else:
            success_signal = self.success()
            if result is None:
                success_signal.emit()
            if isinstance(result, tuple):
                success_signal.emit(*result)
            else:
                success_signal.emit(result)
