from typing import (
    List,
    Optional,
)

from game import item


class Inventory:
    """Represents the inventory."""

    _items: List[Optional[item.Item]] = [None] * 16

    def get_items(self) -> List[Optional[item.Item]]:
        """Get the list of items."""
        return self._items
