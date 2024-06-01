"""
Defines transport items - data transfer objects that are used to
transfer data between task threads and the main thread of Qt application.
"""

from abc import ABC


class AbstractTransportItem(ABC):
    pass