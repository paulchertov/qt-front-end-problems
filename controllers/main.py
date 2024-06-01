from PySide6.QtWidgets import QMainWindow

from model.alchemy.session import OneTimeSessionProvider

from controllers import PSWithViewMixin
from controllers.player import PSPlayerController
from controllers.songs import PSSongsController

from services.song import PSSongService
from indexers.song import SongsIndexer


class PSFrontEndProblems(QMainWindow, PSWithViewMixin):
    """
    Main controller for the application


    """
    gui_name = "main"

    def __init__(self):
        super().__init__()
        self.install_gui()
        self.set_styles()

        # services
        session_provider = OneTimeSessionProvider("db.db")
        songs_index = SongsIndexer()

        self.song_service = PSSongService(session_provider, songs_index)

        # sub-controllers
        self.songs = PSSongsController(self.song_service)
        self.view.workarea.addWidget(self.songs.view)
        self.songs.view.show()

        self.player = PSPlayerController()
        self.view.app_layout.addWidget(self.player.view)
        self.player.view.show()
        # self.player.view.play_switch.clicked.connect(self.test_song_list)

        self.setCentralWidget(self.view)
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("m ^_^ m")
        self.show()


