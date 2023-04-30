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
    _state: Dict[str, Any]

    def __init__(
        self,
        api: scripts.GameAPI,
        sprite_spec: spec.GameSpriteSpec,
        initial_state: Dict[str, Any],
    ):
        super().__init__(name="player", sprite_spec=sprite_spec)

        self._last_activate = 0
        self._api = api
        self._state = initial_state

    def _animation_state(self) -> str:
        next_activate = self._last_activate + ACTIVATE_ANIMATION_LENGTH
        if next_activate > self._api.current_time_secs:
            return "activate"
        return super()._animation_state()

    def on_activate(self) -> None:
        """Triggered when the player is activated."""
        self._last_activate = self._api.current_time_secs

    @property
    def state(self) -> Dict[str, Any]:
        """Gets the state of the player."""
        return self._state

    @state.setter
    def state(self, value: Dict[str, Any]) -> None:
        """Sets the state of the player."""
        self._state = value
