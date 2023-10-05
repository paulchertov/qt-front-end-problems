from typing import List

from PySide6.QtCore import Signal

from model.transport_items.db.lists import SongsListFilters, SongsListSorting
from model.transport_items.db.basic import SongDetailsTransport
from model.transport_items.db.lists import SongListTransport
from model.view_models.song import PSSongModel

from services import PSService
from services.song.indexer import SongsIndexer
from services.song.tasks.single import PSObtainSong
from services.song.tasks.list import PSObtainSongList

from model.alchemy.session import AbstractSessionProvider


class PSSongService(PSService):
    song_obtained = Signal(PSSongModel)
    song_list_obtained = Signal(PSSongModel)
    error_occurred = Signal(Exception)

    def __init__(self, session_provider: AbstractSessionProvider):
        super().__init__(session_provider)
        self.indexer = SongsIndexer()

    def get_by_id(self, id: int):
        """
        Obtains a song by its id
        :param id: Song id
        :return: None

        :emits song_obtained: SongDetailsTransport - obtained song
        :emits error_occurred: Exception - error
        """
        task = PSObtainSong(self.session_provider, id)
        task.song_obtained.connect(self.got_by_id)
        task.error_occurred.connect(self.error_occurred)
        task.run()

    def got_by_id(self, song: SongDetailsTransport):
        """
        Handler for song obtained
        :param song: Song
        :return: None

        :emits song_obtained: PSSongModel - obtained song
        """
        model = self.indexer.add(song)
        self.song_obtained.emit(model)

    def get_list(
        self,
        page: int,
        page_size: int,
        filters: SongsListFilters,
        sortings: SongsListSorting
    ):
        """
        Obtains a list of songs
        :param page: Page number
        :param page_size: Page size
        :param filters: Filters
        :param sortings: Sortings

        :emits song_list_obtained: SongListTransport - list of songs
        :emits error_occurred: Exception - error
        """
        task = PSObtainSongList(
            self.session_provider,
            page,
            page_size,
            filters,
            sortings
        )
        task.song_list_obtained.connect()
        task.error_occurred.connect(self.error_occurred)
        task.run()

    def got_list_songs(self, songs: List[SongDetailsTransport]):
        """
        Handler for songs list obtained
        :param songs: List of songs
        :return: None

        :emits song_list_obtained: List[PSSongModel] - list of songs
        """
        models = [
            self.indexer.add(song)
            for song in songs
        ]
        self.song_list_obtained.emit()
