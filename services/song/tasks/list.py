from PySide6.QtCore import Signal
from sqlalchemy.sql import select, func, Selectable
from sqlalchemy.orm import Session

from model.alchemy.session import AbstractSessionProvider
from model.alchemy.tables import (
    Song, Artist, Genre, SongFile, Tag
)

from model.transport_items.db.lists import (
    DBSortingDirection,
    SongsListSorting, SongsListFilters, SongListTransport
)
from tasks.db import PSDBTask
from services.adapters.db_to_trans_lists import song_list_to_transport


class PSObtainSongList(PSDBTask):
    """
    Task to obtain a list of songs
        signals:
            song_list_obtained: Signal to emit the obtained song list
            error: Signal to emit an error
        fields:
            :str id: task id
            :int page: currently selected page
            :int page_size: number of items per page
            :SongsListFilters filters: filters to apply to the list
            :SongsListSorting sortings: sortings to apply to the list

            All fields are required in the constructor
        methods:
            :Signal success(): service method defined to point on a signal to emit see
            :SongListTransport : query to get the song list
            :Selectable add_filters_and_sortings(Selectable query): adds filters and sortings to the query
    """
    song_list_obtained = Signal(SongListTransport)

    def __init__(
        self,
        id: str,
        session_provider: AbstractSessionProvider,
        page: int,
        page_size: int,
        filters: SongsListFilters,
        sortings: SongsListSorting
    ):
        super().__init__(id, session_provider)
        self.page = page
        self.page_size = page_size
        self.filters = filters
        self.sortings = sortings

    def success(self) -> Signal:
        """
        On success signal song_list_obtained is emitted
        """
        return self.song_list_obtained

    def query(self, session: Session) -> SongListTransport:
        """
        Query to get the song list

        :param session: session to execute the query
        :return: SongListTransport
        """
        count_query = select(func.count(Song.id.distinct())).\
            select_from(Song).\
            outerjoin(Song.artist).\
            outerjoin(Song.file).\
            outerjoin(Song.tags).\
            outerjoin(Song.genres)
        count_query = self.add_filters_and_sortings(count_query)

        unique_song_ids = select(Song.id.distinct()).\
            select_from(Song).\
            outerjoin(Song.artist).\
            outerjoin(Song.file).\
            outerjoin(Song.tags).\
            outerjoin(Song.genres)
        unique_song_ids = self.add_filters_and_sortings(unique_song_ids). \
            limit(self.page_size). \
            offset(self.page_size * self.page)
        unique_song_ids = {id[0] for id in session.execute(unique_song_ids).all()}

        cnt = session.execute(count_query).scalar()
        if not (cnt and unique_song_ids):
            entities = []
        else:
            query = select(
                Song,
                Artist,
                SongFile,
                Tag,
                Genre
            ). \
                outerjoin(Song.artist). \
                outerjoin(Song.file). \
                outerjoin(Song.tags). \
                outerjoin(Song.genres). \
                where(Song.id.in_(unique_song_ids))

            entities = session.execute(query).all()
            entities = [entity.tuple() for entity in entities]

        return song_list_to_transport(
            entities,
            self.page,
            self.page_size,
            cnt,
            self.filters,
            self.sortings
        )

    def add_filters_and_sortings(self, query: Selectable):
        if self.filters.artist_id is not None:
            query = query.where(Song.artist_id == self.filters.artist_id)
        if self.filters.genre_id is not None:
            query = query.where(Genre.id == self.filters.genre_id)
        if self.filters.tag_id is not None:
            query = query.where(Tag.id == self.filters.tag_id)
        if self.filters.liked is not None:
            query = query.where(Song.liked == self.filters.liked)

        if self.sortings.name is not None:
            sort = SongFile.duration
            if self.sortings.name != DBSortingDirection.ASC:
                sort = sort.desc()
            query = query.order_by(sort)
        if self.sortings.duration is not None:
            sort = SongFile.duration
            if self.sortings.duration != DBSortingDirection.ASC:
                sort = sort.desc()
            query = query.order_by(sort)
        return query
