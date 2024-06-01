from indexers import AbstractIndexer

from model.view_models.song import PSSongModel
from model.transport_items.db.basic import SongDetailsTransport


class ArtistsIndexer(AbstractIndexer[int, SongDetailsTransport, PSSongModel]):
    def obtain_id(self, obj: SongDetailsTransport) -> int:
        return obj.id

    def create_object(self, obj: SongDetailsTransport) -> PSSongModel:
        return PSSongModel(obj)

    def update_object(self, obj: SongDetailsTransport, model: PSSongModel):
        model.set_from_transport(obj)
