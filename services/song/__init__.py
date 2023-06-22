from typing import Callable

from PySide6.QtCore import Signal

from model.transport_items.db.lists import SongsListFilters, SongsListSorting
from model.transport_items.db.basic import SongDetailsTransport
from model.transport_items.db.lists import SongListTransport
from services import PSService
from services.song.tasks.single import PSObtainSong
from services.song.tasks.list import PSObtainSongList


class PSSongService(PSService):
    song_obtained = Signal(SongDetailsTransport)
    song_list_obtained = Signal(SongListTransport)
    error_occurred = Signal(Exception)

    def get_by_id(self, id: int):
        task = PSObtainSong(self.session_provider, id)
        task.song_obtained.connect(self.song_obtained)
        task.error_occurred.connect(self.error_occurred)
        task.run()

    def get_list(
        self,
        page: int,
        page_size: int,
        filters: SongsListFilters,
        sortings: SongsListSorting
    ):
        task = PSObtainSongList(
            self.session_provider,
            page,
            page_size,
            filters,
            sortings
        )
        task.song_list_obtained.connect(self.song_list_obtained)
        task.error_occurred.connect(self.error_occurred)
        task.run()
