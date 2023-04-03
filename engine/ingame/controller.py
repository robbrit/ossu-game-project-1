from typing import (
    Dict,
)

import arcade

from engine import (
    model,
    view,
)


class InGameController:
    """
    This class represents the controller layer. It manages interaction between
    the game and the user.
    """

    model: model.Model
    view: view.View
    keys: Dict[int, bool]

    def __init__(self, model: model.Model, view: view.View):
        self.model = model
        self.view = view

        self.keys = {}

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.keys[symbol] = True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.keys[symbol] = False

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        wx, wy = self.view.to_world_coords(screen_x, screen_y)

        player_dx = wx - self.model.player_sprite.center_x
        player_dy = wy - self.model.player_sprite.center_y

        self.model.set_player_facing(player_dx, player_dy)

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handles when the user releases a mouse button."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            # We activate when the right mouse button is hit.
            self.model.activate()

    def on_update(self, delta_time: int) -> None:
        """
        Updates player speed based on keypress,
        and prevents player going out-of-bounds.
        """
        vx, vy = 0, 0

        player_sprite = self.model.player_sprite
        map_width = self.model.width * self.model.tile_width
        map_height = self.model.height * self.model.tile_height

        if (self._up_key_pressed() and not
        (player_sprite.top >= map_height)):
            vy += 1
        if (self._down_key_pressed() and not
        (player_sprite.bottom <= 0)):
            vy -= 1

        if (self._left_key_pressed() and not
        (player_sprite.left <= 0)):
            vx -= 1
        if (self._right_key_pressed() and not
        (player_sprite.right >= map_width)):
            vx += 1

        self.model.set_player_speed(vx=vx, vy=vy)

    def _up_key_pressed(self) -> bool:
        return self.keys.get(arcade.key.UP) or self.keys.get(arcade.key.W)

    def _down_key_pressed(self) -> bool:
        return self.keys.get(arcade.key.DOWN) or self.keys.get(arcade.key.S)

    def _left_key_pressed(self) -> bool:
        return self.keys.get(arcade.key.LEFT) or self.keys.get(arcade.key.A)

    def _right_key_pressed(self) -> bool:
        return self.keys.get(arcade.key.RIGHT) or self.keys.get(arcade.key.D)
