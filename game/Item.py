import enum
from typing import (
    Protocol,
)


class ItemType(enum.Enum):
    WEAPON: 0
    OTHER: 1


class Item:
    """Protocol to define an Item."""

    _asset: str
    _itemType: ItemType

    def __init__(self, asset, item_type):
        """Initialize the Item with an asset and a type"""
