from typing import (
    Any,
    Dict,
)


class Health:
    """Class to track the health of an entity."""

    def __init__(self, initial_hp: int):
        self.max_hp = initial_hp
        self.hp = initial_hp

    def adjust(self, health: int):
        """Adjusts the health by a certain amount."""
        self.hp = max(0, min(self.hp + health, self.max_hp))

    @property
    def state(self) -> Dict[str, Any]:
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
        }

    @state.setter
    def state(self, value: Dict[str, Any]) -> None:
        self.hp = int(value["hp"])
        self.max_hp = int(value["hp"])

    @property
    def is_dead(self) -> bool:
        """Determines if the entity is dead."""
        return self.hp <= 0
