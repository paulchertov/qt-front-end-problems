"""
This module contains dataclasses for transport items for listings
of database entities.
Classes:
    SongsListFilters: Filters for song listing
    SongsListSorting: Sorting for song listing
    SongListTransport: Transport item for song listing
"""
from typing import Optional
from dataclasses import dataclass

from model.transport_items.db import (
    AbstractDBFilters, AbstractDBSorting,
    AbstractDBTransportList, DBSortingDirection
)


@dataclass(slots=True)
class SongsListFilters(AbstractDBFilters):
    tag_id: Optional[int]
    genre_id: Optional[int]
    artist_id: Optional[int]
    liked: Optional[bool]


@dataclass(slots=True)
class SongsListSorting(AbstractDBSorting):
    name: Optional[DBSortingDirection]
    duration: Optional[DBSortingDirection]


@dataclass(slots=True)
class SongListTransport(AbstractDBTransportList):
    filters: SongsListFilters
    sortings: SongsListSorting

