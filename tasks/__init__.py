"""
"""
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal


class PSTask(QThread):
    """

    """
    error_occurred = Signal(Exception)
