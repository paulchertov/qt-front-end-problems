from typing import List, Callable
import string

from model.alchemy.session import AbstractSessionProvider

from model.transport_items.db.lists import SongsListFilters, SongsListSorting
from model.transport_items.db.basic import SongDetailsTransport
from model.view_models.song import PSSongModel

from services import PSDbService
from indexers.song import SongsIndexer
from services.song.tasks.single import PSObtainSong
from services.song.tasks.list import PSObtainSongList

from utils.random import random_string_prepare


class PSSongService(PSDbService):
    """
    Service for obtaining songs

    Signals:
        :emits song_obtained: PSSongModel - obtained song
        :emits song_list_obtained: List[PSSongModel] - obtained list of songs
        :emits error_occurred: Exception - error

    Fields:
        :session_provider: Session provider
        :indexer: Indexer for songs
        :generate_task_id: Callable[[], str] - function to generate task id,
            basically we do not use task ids, current implementation uses callbacks
            to handle the results, but I want to keep things as less opinionated as possible
            so it is possible to use task objects and therefore ids later
    Methods:
        :get_by_id: Obtains a song by its id
        :get_list: Obtains a list of songs
        :process_single: Mapper from SongDetailsTransport to PSSongModel
        :process_list: Handler for songs list obtained
    """
    def __init__(
        self,
        session_provider: AbstractSessionProvider,
        indexer: SongsIndexer
    ):
        super().__init__(session_provider)
        self.indexer = indexer
        self.generate_task_id = random_string_prepare(
            32,
            string.ascii_letters + string.digits
        )

    def get_by_id(
        self,
        id: int,
        callback: Callable[[PSSongModel], None],
        error_callback: Callable[[Exception], None]
    ) -> None:
        """
        Obtains a song by its id
        Song is never returned, it is used in the provided callback

        :param id: Song id
        :param callback: Success Callback function
        :param error_callback: Error callback function
        :return: None

        :emits song_obtained: SongDetailsTransport - obtained song
        :emits error_occurred: Exception - error
        """
        task = PSObtainSong(
            self.generate_task_id(),
            self.session_provider,
            id
        )
        task.song_obtained.connect(
            lambda song: callback(self.process_single(song))
        )

        task.error_occurred.connect(error_callback)
        task.run()

    def process_single(self, song: SongDetailsTransport) -> PSSongModel:
        """
        Mapper from SongDetailsTransport to PSSongModel
        :param song: Song
        :return: PSSongModel
        """
        return self.indexer.add(song)

    def get_list(
        self,
        page: int,
        page_size: int,
        filters: SongsListFilters,
        sortings: SongsListSorting,
        callback: Callable[[List[PSSongModel]], None],
        error_callback: Callable[[Exception], None]
    ):
        """
        Obtains a list of songs
        :param page: Page number
        :param page_size: Page size
        :param filters: Filters
        :param sortings: Sortings
        :param callback: Success callback function
        :param error_callback: Error callback function
        """
        task = PSObtainSongList(
            self.generate_task_id(),
            self.session_provider,
            page,
            page_size,
            filters,
            sortings
        )

        task.song_list_obtained.connect(
            lambda song_list: callback(self.process_list(song_list))
        )
        task.error_occurred.connect(error_callback)

        task.run()

    def process_list(self, songs: List[SongDetailsTransport]) -> List[PSSongModel]:
        """
        Handler for songs list obtained
        :param songs: List of songs
        :return:
        """
        return [
            self.indexer.add(song)
            for song in songs
        ]

