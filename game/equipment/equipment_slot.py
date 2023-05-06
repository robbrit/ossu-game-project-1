from typing import (
    Optional,
)

from game import item


class EquipmentSlot:
    """Represents a equipment slot."""

    _item: Optional[item.Item]
    _valid_types: set[item.ItemType]

    def __init__(self, _item: item.Item, valid_types: set[item.ItemType]):
        self._item = _item
        self._valid_types = valid_types

    def equip_item(self, _item: item.Item):
        """Equips an item if it's a valid type."""

        if _item.item_type in self._valid_types:
            self._item = _item
