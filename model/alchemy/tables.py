from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Text, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.alchemy import Base


song_genres = Table(
    "song_genres",
    Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)


song_tags = Table(
    "song_tags", Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    songs: Mapped[List[Song]] = relationship(
        "Song",
        back_populates="artist"
    )


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    songs: Mapped[List[Song]] = relationship(
        "Song",
        secondary=song_genres,
        back_populates="genres"
    )


class SongFile(Base):
    __tablename__ = "song_files"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    duration: Mapped[int] = mapped_column()

    song: Mapped[Song | None] = relationship(
        "Song",
        back_populates="file"
    )


class Song(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    liked: Mapped[bool] = mapped_column(default=False)

    file_id: Mapped[int] = mapped_column(
        "SongFile",
        ForeignKey("song_files.id")
    )
    artist_id: Mapped[int] = mapped_column(
        "Artist",
        ForeignKey("artists.id")
    )

    artist: Mapped[Artist] = relationship(
        back_populates="songs"
    )
    file: Mapped[SongFile] = relationship(
        back_populates="song"
    )
    genres: Mapped[List[Genre]] = relationship(
        secondary=song_genres,
        back_populates="songs"
    )
    tags: Mapped[List[Tag]] = relationship(
        secondary=song_tags,
        back_populates="songs"
    )


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    songs: Mapped[List[Song]] = relationship(
        secondary=song_tags,
        back_populates="tags"
    )
