from typing import (
    Dict,
)

import arcade

from engine import (
    scripts,
    view,
)
from engine.model import world


class InGameController:
    """
    This class represents the controller layer. It manages interaction between
    the game and the user.
    """

    _world: world.World
    _view: view.View
    _keys: Dict[int, bool]
    _api: scripts.GameAPI
    _menu_gui: scripts.GUI

    def __init__(
        self,
        _world: world.World,
        _view: view.View,
        menu_gui: scripts.GUI,
        api: scripts.GameAPI,
    ):
        self._world = _world
        self._view = _view

        self._keys = {}
        self._menu_gui = menu_gui
        self._api = api

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles when a key is pressed."""
        # pylint: disable=unused-argument
        self._keys[symbol] = True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles when a key is released."""
        # pylint: disable=unused-argument
        self._keys[symbol] = False

        if symbol == arcade.key.ESCAPE:
            self._api.show_gui(self._menu_gui)

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        """Handles when the mouse is moved."""
        # pylint: disable=unused-argument
        world_x, world_y = self._view.to_world_coords(screen_x, screen_y)

        player_dx = world_x - self._world.player_sprite.center_x
        player_dy = world_y - self._world.player_sprite.center_y

        self._world.set_player_facing(player_dx, player_dy)

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handles when the user releases a mouse button."""
        # pylint: disable=unused-argument

        if button == arcade.MOUSE_BUTTON_RIGHT:
            # We activate when the right mouse button is hit.
            self._world.activate()

        if button == arcade.MOUSE_BUTTON_LEFT:
            # We attack when the left mouse button is hit.
            self._world.hit()

    def on_update(self, delta_time: float) -> None:
        """Updates the world."""
        # pylint: disable=unused-argument
        vx, vy = 0, 0

        if self._up_key_pressed():
            vy += 1
        if self._down_key_pressed():
            vy -= 1

        if self._left_key_pressed():
            vx -= 1
        if self._right_key_pressed():
            vx += 1

        self._world.set_player_speed(vx=vx, vy=vy)

    def _up_key_pressed(self) -> bool:
        return self._keys.get(arcade.key.UP) or self._keys.get(arcade.key.W) or False

    def _down_key_pressed(self) -> bool:
        return self._keys.get(arcade.key.DOWN) or self._keys.get(arcade.key.S) or False

    def _left_key_pressed(self) -> bool:
        return self._keys.get(arcade.key.LEFT) or self._keys.get(arcade.key.A) or False

    def _right_key_pressed(self) -> bool:
        return self._keys.get(arcade.key.RIGHT) or self._keys.get(arcade.key.D) or False
