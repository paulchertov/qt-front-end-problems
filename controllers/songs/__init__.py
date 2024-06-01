from PySide6.QtCore import QObject, Signal

from controllers import PSWithViewMixin
from controllers.songs.detail import SongDetails

from services.song import PSSongService
from model.transport_items.db.lists import SongsListFilters, SongsListSorting


class PSSongsController(QObject, PSWithViewMixin):
    gui_name = "songs/main"

    def __init__(self, service: PSSongService):
        super().__init__()
        self.install_gui()

        self.__service = service
        self.detail = SongDetails()

        self.set_styles()

    def test_song_service(self):
        self.__service.get_by_id(12)

    def test_song_list(self):
        self.__service.get_list(
            1,
            10,
            SongsListFilters(
                tag_id=None,
                genre_id=None,
                artist_id=None,
                liked=None
            ),
            SongsListSorting(
                name=None,
                duration=None
            ),
            self.got_song_list,
            self.song_error
        )

    def song_error(self, err):
        raise err

    def got_song(self, entity):
        print(type(entity))
        print(type(entity.artist))

    def got_song_list(self, result):
        print(result)
        print(len(result))