"""
This module contains transport items for basic entities.
Classes:
    LinkItemTransport: Transport item for entities consisting of
        a name and an ID.
    ArtistTransport, TagTransport, GenreTransport, SongFileTransport:
        are just LinkItemTransport
    SongDetailsTransport: Transport item for song details
        containing related entities.
"""
from typing import List
from dataclasses import dataclass

from model.transport_items.db import AbstractDBTransportItem


@dataclass(slots=True)
class LinkItemTransport(AbstractDBTransportItem):
    name: str


@dataclass(slots=True)
class ArtistTransport(LinkItemTransport):
    pass


@dataclass(slots=True)
class TagTransport(LinkItemTransport):
    pass


@dataclass(slots=True)
class GenreTransport(LinkItemTransport):
    pass


@dataclass(slots=True)
class SongFileTransport(AbstractDBTransportItem):
    duration: int


@dataclass(slots=True)
class SongDetailsTransport(LinkItemTransport):
    liked: bool

    artist: LinkItemTransport
    file: SongFileTransport

    tags: List[LinkItemTransport]
    genres: List[LinkItemTransport]
