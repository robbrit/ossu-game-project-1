from typing import (
    Dict,
)

import arcade

from engine import model


class InGameController:
    """
    This class represents the controller layer. It manages interaction between
    the game and the user.
    """

    model: model.Model
    keys: Dict[int, bool]

    def __init__(self, model: model.Model):
        self.model = model

        self.keys = {}

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.keys[symbol] = True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.keys[symbol] = False

    def on_update(self, delta_time: int) -> None:
        vx, vy = 0, 0

        if self._up_key_pressed():
            vy += 1
        if self._down_key_pressed():
            vy -= 1

        if self._left_key_pressed():
            vx -= 1
        if self._right_key_pressed():
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
