from typing import (
    Optional,
)

from item import (
    Item,
    ItemType,
)


class EquipmentSlot:
    """Represents a equipment slot."""

    _item: Optional[Item]
    _valid_types: set[ItemType]

    def __init__(self, item: Item, valid_types: set[ItemType]):
        self._item = item
        self._valid_types = valid_types

    def equip_item(self, item: Item):
        """Equips an item if it's a valid type."""

        if item.item_type in self._valid_types:
            self._item = item
