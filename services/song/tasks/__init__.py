from typing import Any, Optional, List

from PySide6.QtCore import Signal
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, joinedload

from model.alchemy.session import AbstractSessionProvider
from model.alchemy.tables import (
    Song, SongFile, Artist, Genre, Tag
)
from model.transport_items.db.basic import (
    GenreTransport, TagTransport,
    ArtistTransport, SongFileTransport, SongDetailsTransport
)
from tasks.db import PSDBTask
from services.adapters.db_to_trans import song_db_to_trans


class PSObtainSong(PSDBTask):
    song_obtained = Signal(SongDetailsTransport)

    def __init__(self, session_provider: AbstractSessionProvider, song_id: int):
        super().__init__(session_provider)
        self.song_id = song_id

    def success(self) -> Signal:
        return self.song_obtained

    def query(self, session: Session) -> SongDetailsTransport:
        query = select(Song).options(
            joinedload(Song.artist),
            joinedload(Song.file),
            joinedload(Song.tags),
            joinedload(Song.genres)
        ).where(Song.id == self.song_id)
        entity = session.execute(query).first()
        if entity is not None:
            result = song_db_to_trans(entity[0])
            return result
        raise IndexError(f"Song with id `{self.song_id}` was not found")