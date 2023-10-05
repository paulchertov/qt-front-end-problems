from os import path

from PySide6.QtCore import QObject, Signal

from controllers import PSWithViewMixin
from services.song import PSSongService


class SongDetails(QObject, PSWithViewMixin):
    to_play = Signal(int)
    gui_name_template = path.join("gui", "songs")
    gui_name = "detail"

    def __init__(self, songs_service: "PSSongService"):
        super().__init__()
        self.install_gui()
        self.set_styles()
        self.song_service = songs_service





