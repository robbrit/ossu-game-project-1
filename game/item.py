import enum
from typing import (
    Protocol,
)


class ItemType(enum.Enum):
    """Represents the item types."""

    WEAPON: 0
    OTHER: 1


class Item(Protocol):
    """Protocol to define an Item."""

    _asset: str
    _name: str
    item_type: ItemType
