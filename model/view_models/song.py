from typing import List, Iterable, Tuple

from model.view_models import PSViewModel, ViewModelField
from model.transport_items.db.basic import (
    SongDetailsTransport, GenreTransport, TagTransport
)


class PSSongModel(PSViewModel):
    """
    View model for song entity
    """

    liked: ViewModelField()

    artist: ViewModelField()

    duration: ViewModelField()

    def __init__(self, song: SongDetailsTransport):
        super().__init__()
        with self.update(silent=True):
            self.set_from_transport(song)

    def set_from_transport(self, song: SongDetailsTransport):
        """
        Sets data from transport item
        :param song: Song transport item
        """
        self.liked = song.liked
        self.artist = song.artist.name
        self.duration = song.file.duration
