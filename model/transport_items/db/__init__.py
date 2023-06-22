from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

from model.transport_items import AbstractTransportItem


@dataclass(slots=True)
class AbstractDBTransportItem(AbstractTransportItem):
    id: int


class AbstractDBFilters:
    pass


class AbstractDBSorting:
    pass


class DBSortingDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(slots=True)
class AbstractDBTransportList(AbstractTransportItem):
    size: int
    page: int
    page_size: int
    sortings: AbstractDBSorting
    filters: AbstractDBFilters
    items: List[AbstractDBTransportItem]
