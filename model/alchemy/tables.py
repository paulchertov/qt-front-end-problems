from sqlalchemy import Column, Integer, String, Boolean, Text

from model.alchemy import Base


class Artist(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Genre(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class SongFile(Base):
    id = Column(Integer, primary_key=True)
    duration = Column(Integer)


class Song(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    liked = Column(Boolean)


class Tag(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
