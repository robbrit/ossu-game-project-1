from typing import (
    Optional,
)

from item import (
    Item,
    ItemType,
)


class Inventory:
    """Represents the inventory."""

    _items: list[Optional[Item]] = [None] * 16
