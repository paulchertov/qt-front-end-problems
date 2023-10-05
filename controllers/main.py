from PySide6.QtWidgets import QMainWindow

from model.alchemy.session import OneTimeSessionProvider

from controllers import PSWithViewMixin
from controllers.player import PSPlayerController

from services.song import PSSongService
from model.transport_items.db.lists import SongsListFilters, SongsListSorting


class PSFrontEndProblems(QMainWindow, PSWithViewMixin):
    gui_name = "main"

    def __init__(self):
        super().__init__()
        self.install_gui()
        self.set_styles()

        # services
        session_provider = OneTimeSessionProvider("db.db")

        self.song_service = PSSongService(session_provider)
        self.song_service.error_occurred.connect(self.song_error)
        self.song_service.song_obtained.connect(self.got_song)
        self.song_service.song_list_obtained.connect(self.got_song_list)

        # sub-controllers
        self.player = PSPlayerController()
        self.player.view.play_switch.clicked.connect(self.test_song_list)

        self.view.app_layout.addWidget(self.player.view)
        self.player.view.show()
        self.setCentralWidget(self.view)
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("m ^_^ m")
        self.show()


