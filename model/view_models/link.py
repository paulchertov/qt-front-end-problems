from typing import List, Iterable, Tuple

from model.view_models import PSViewModel, ViewModelField
from model.transport_items.db.basic import LinkItemTransport


class PSLinkModel(PSViewModel):
    """
    View model for link entity (name - id pair)
    """

    id: int
    name: ViewModelField()

    def __init__(self, link_item: LinkItemTransport):
        super().__init__()
        with self.update(silent=True):
            self.set_from_transport(link_item)

    def set_from_transport(self, link_item: LinkItemTransport):
        """
        Sets data from transport item
        :param song: Song transport item
        """
        self.id = link_item.id
        self.name = link_item.name
