from typing import (
    Optional,
    Tuple,
)

import arcade
import arcade.tilemap

from engine import model

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "OSSU Game Project"


class View:
    """
    Main view class. This manages rendering things to the screen.
    """

    width: int
    height: int
    model: model.Model
    camera: Optional[arcade.Camera]

    def __init__(self, model: model.Model):
        self.width = 0
        self.height = 0
        self.model = model
        self.camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, size: Tuple[int, int]) -> None:
        self.camera = arcade.Camera(size[0], size[1])
        self.width = self.model.tile_map.width * self.model.tile_map.tile_width
        self.height = self.model.tile_map.height * self.model.tile_map.tile_height

    def on_draw(self) -> None:
        self.camera.use()
        self.model.scene.draw()

    def on_update(self, delta_time: int) -> None:
        self._center_camera_to_player()

    def _center_camera_to_player(self) -> None:
        player = self.model.player_sprite

        v_width = self.camera.viewport_width
        v_height = self.camera.viewport_height

        screen_center_x = min(
            self.width - v_width,
            max(
                0,
                player.center_x - v_width / 2,
            ),
        )
        screen_center_y = min(
            self.height - v_height,
            max(
                0,
                player.center_y - v_height / 2,
            ),
        )

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
