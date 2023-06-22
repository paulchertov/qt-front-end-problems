from typing import List
from dataclasses import dataclass

from model.transport_items.db import AbstractDBTransportItem


@dataclass(slots=True)
class ArtistTransport(AbstractDBTransportItem):
    name: str


@dataclass(slots=True)
class TagTransport(AbstractDBTransportItem):
    name: str


@dataclass(slots=True)
class GenreTransport(AbstractDBTransportItem):
    name: str


@dataclass(slots=True)
class SongFileTransport(AbstractDBTransportItem):
    duration: int


@dataclass(slots=True)
class SongDetailsTransport(AbstractDBTransportItem):
    name: str
    liked: bool

    artist: ArtistTransport
    file: SongFileTransport

    tags: List[TagTransport]
    genres: List[GenreTransport]
