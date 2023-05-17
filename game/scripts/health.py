from typing import (
    Any,
    cast,
    Dict,
)

from engine import scripts
from engine.model import player_sprite


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


INVINCIBLE_TIME = 1.5


class DamagesPlayer(scripts.SavesAPI):
    """Class to handle damaging the player."""

    _damage: int
    _last_damage_time: float

    def __init__(self, damage: int):
        scripts.SavesAPI.__init__(self)
        self._damage = damage
        self._last_damage_time = 0.0

    def on_collide(self, owner: scripts.ScriptOwner, other: scripts.Entity) -> None:
        """Triggered when the owner collides with another entity."""
        assert self.api is not None

        if not isinstance(other, player_sprite.PlayerSprite):
            return

        if self.api.current_time_secs < self._last_damage_time + INVINCIBLE_TIME:
            return

        if owner.is_dying:
            return

        data = self.api.player_data
        hp = cast(Health, data["hp"])

        hp.adjust(-self._damage)
        self._last_damage_time = self.api.current_time_secs
        self.api.player_data["last_damage_time"] = self._last_damage_time
