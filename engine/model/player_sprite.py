from engine import scripts
from engine.model import game_sprite

ACTIVATE_ANIMATION_LENGTH = 0.25


class PlayerSprite(game_sprite.GameSprite):
    """Represents the player in the game."""

    _last_activate: int
    _api: scripts.GameAPI

    def __init__(self, api: scripts.GameAPI, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._last_activate = 0
        self._api = api

    def _animation_state(self) -> str:
        next_activate = self._last_activate + ACTIVATE_ANIMATION_LENGTH
        if next_activate > self._api.current_time_secs:
            return "activate"
        return super()._animation_state()

    def on_activate(self) -> None:
        """Triggered when the player is activated."""
        self._last_activate = self._api.current_time_secs
