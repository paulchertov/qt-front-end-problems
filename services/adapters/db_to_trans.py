from model.alchemy.tables import Song, SongFile, Artist, Tag, Genre
from model.transport_items.db.basic import (
    SongDetailsTransport,
    TagTransport, ArtistTransport, SongFileTransport, GenreTransport
)


def song_db_to_trans(entity: Song) -> SongDetailsTransport:
    """
    Converts a song from the database to a transport item
    """
    if entity.artist is not None:
        artist = artist_db_to_trans(entity.artist)
    else:
        artist = None

    if entity.file is not None:
        file = file_db_to_trans(entity.file)
    else:
        file = None

    genres = [
        genre_db_to_trans(genre)
        for genre in (entity.genres or [])
    ]

    tags = [
        tag_db_to_trans(tag)
        for tag in (entity.tags or [])
    ]

    return SongDetailsTransport(
        id=entity.id,
        name=entity.name,
        liked=entity.liked,
        artist=artist,
        genres=genres,
        file=file,
        tags=tags
    )


def artist_db_to_trans(entity: Artist) -> ArtistTransport:
    """
    Converts an artist from the database to a transport item
    """
    return ArtistTransport(
        id=entity.id,
        name=entity.name
    )


def file_db_to_trans(entity: SongFile) -> SongFileTransport:
    """
    Converts a song file from the database to a transport item
    """
    return SongFileTransport(
        id=entity.id,
        duration=entity.duration
    )


def tag_db_to_trans(entity: Tag) -> TagTransport:
    """
    Converts a tag from the database to a transport item
    """
    return TagTransport(id=entity.id, name=entity.name)


def genre_db_to_trans(entity: Genre) -> GenreTransport:
    """
    Converts a genre from the database to a transport item
    """
    return GenreTransport(id=entity.id, name=entity.name)

