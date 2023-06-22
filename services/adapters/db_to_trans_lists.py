from typing import List, Tuple, Dict

from model.alchemy.tables import Song, SongFile, Artist, Tag, Genre
from model.transport_items.db.basic import (
    SongDetailsTransport,
    TagTransport, ArtistTransport, SongFileTransport, GenreTransport
)
from model.transport_items.db.lists import SongListTransport, SongsListSorting, SongsListFilters

SongListQueryRow = Tuple[Song, Artist, SongFile, Tag, Genre]


def _song_list_item(
    current_song: Song,
    current_artist: Artist,
    genres: Dict[int, Genre],
    tags: Dict[int, Tag],
    file: SongFile
) -> SongDetailsTransport:
    """
    Internal use only function to convert a song list item from
    several database entities to a transport item

    :param current_song: Song entity
    :param current_artist: Artist entity
    :param genres: Dictionary of genres
    :param tags: Dictionary of tags
    :param file: Song file entity

    :return: Song transport item
    """
    return SongDetailsTransport(
        id=current_song.id,
        name=current_song.name,
        liked=current_song.liked,
        artist=ArtistTransport(
            id=current_artist.id,
            name=current_artist.name
        ) if current_artist is not None else None,
        genres=[
            GenreTransport(
                id=genre.id,
                name=genre.name
            )
            for genre in genres.values()
        ],
        tags=[
            TagTransport(
                id=tag.id,
                name=tag.name
            )
            for tag in tags.values()
        ],
        file=SongFileTransport(
            id=file.id,
            duration=file.duration
        ) if file is not None else None
    )


def song_list_to_transport(
    rows: List[SongListQueryRow],
    page: int,
    page_size: int,
    size: int,
    filters: SongsListFilters,
    sortings: SongsListSorting
) -> SongListTransport:
    result = []

    current_song = None
    current_artist = None
    current_file = None
    genres = {}
    tags = {}

    for song, artist, file, tag, genre in rows:

        if current_song is None:
            current_song = song
            current_artist = artist
            current_file = file
        elif current_song.id != song.id:
            result.append(
                _song_list_item(
                    current_song=current_song,
                    current_artist=current_artist,
                    genres=genres,
                    tags=tags,
                    file=current_file
                )
            )
            current_song = song
            current_artist = artist
            current_file = file
            genres = {}
            tags = {}

        if tag is not None:
            tags[tag.id] = tag
        if genre is not None:
            genres[genre.id] = genre

    if current_song is not None:
        result.append(
            _song_list_item(
                current_song=current_song,
                current_artist=current_artist,
                genres=genres,
                tags=tags,
                file=current_file
            )
        )
    return SongListTransport(
        items=result,
        page=page,
        page_size=page_size,
        size=size,
        filters=filters,
        sortings=sortings
    )

