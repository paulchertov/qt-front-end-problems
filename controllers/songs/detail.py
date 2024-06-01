from os import path
from typing import Optional

from PySide6.QtCore import QObject, Signal

from controllers import PSWithViewMixin
from model.view_models.song import PSSongModel


class SongDetails(QObject, PSWithViewMixin):
    to_play = Signal(int)
    gui_name_template = path.join("gui", "songs")
    gui_name = "detail"

    def __init__(self):
        super().__init__()
        self.install_gui()
        self.set_styles()

        self.__model: Optional[PSSongModel] = None
        self.__model.updated.connect(self.update_view)

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if self.__model is not None:
            self.__model.updated.disconnect(self.update_view)

        self.__model = value
        self.__model.updated.connect(self.update_view)
        self.update_view()

    def update_view(self):
        self.view.title.setText(
            self.__model.name if self.__model is not None else ""
        )
        self.view.liked.setChecked(
            self.__model.liked if self.__model is not None else False
        )
        self.view.artist_link.setText(
            self.__model.artist if self.__model is not None else ""
        )

        if self.__model is not None:
            self.view.artist_link.clicked.connect(
                self.__model.artist_clicked
            )
        else:
            self.view.artist_link.clicked.enabled = False





