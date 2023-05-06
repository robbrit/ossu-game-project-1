from typing import (
    Optional,
)

from game import item


class Inventory:
    """Represents the inventory."""

    _items: list[Optional[item.Item]] = [None] * 16
