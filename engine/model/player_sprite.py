from typing import (
    Any,
    Dict,
)

from engine import (
    scripts,
    spec,
)
from engine.model import game_sprite

ACTIVATE_ANIMATION_LENGTH = 0.25


class PlayerSprite(game_sprite.GameSprite):
    """Represents the player in the game."""

    _last_activate: float
    _api: scripts.GameAPI
    _data: Dict[str, Any]

    def __init__(
        self,
        api: scripts.GameAPI,
        sprite_spec: spec.GameSpriteSpec,
        initial_data: Dict[str, Any],
    ):
        super().__init__(name="player", sprite_spec=sprite_spec)

        self._last_activate = 0
        self._api = api
        self._data = initial_data

    def _animation_state(self) -> str:
        next_activate = self._last_activate + ACTIVATE_ANIMATION_LENGTH
        if next_activate > self._api.current_time_secs:
            return "activate"
        return super()._animation_state()

    def on_activate(self) -> None:
        """Triggered when the player is activated."""
        self._last_activate = self._api.current_time_secs

    @property
    def data(self) -> Dict[str, Any]:
        """Gets the data for the player."""
        return self._data

    @data.setter
    def data(self, value: Dict[str, Any]) -> None:
        """Sets the data for the player."""
        self._data = value

    @property
    def state(self) -> game_sprite.SpriteState:
        """Gets the state of the player."""
        base = super().state
        base.data = self._data
        return base
