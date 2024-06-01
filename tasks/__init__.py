"""
Module for tasks, tasks are operations that are executed in separate thread

classes:
    PSTask - abstract class for task
modules:
    db - tasks to work with database
"""
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal


class PSTask(QThread):
    """
    Abstract class for task, subclass must implement method
    signals: error_occurred(Exception) - emits Exception that occurred

    properties:
        id - id to identify particular task
    """
    error_occurred = Signal(Exception)

    def __init__(self, id: str):
        super().__init__()
        self.__id = id

    @property
    def id(self) -> str:
        return self.__id
