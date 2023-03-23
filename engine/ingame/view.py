from typing import (
    Optional,
    Tuple,
)

import arcade
import arcade.tilemap

from engine import model


class InGameView:
    """
    Main view class. This manages rendering things to the screen.
    """

    width: int
    height: int
    model: model.Model
    camera: Optional[arcade.Camera]

    def __init__(self, model: model.Model, viewport_size: Tuple[int, int]):
        self.width = 0
        self.height = 0
        self.model = model
        self.camera = None

        self.viewport_size = viewport_size

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self) -> None:
        self.camera = arcade.Camera(
            self.viewport_size[0],
            self.viewport_size[1],
        )
        self.width = self.model.tile_map.width * self.model.tile_map.tile_width
        self.height = self.model.tile_map.height * self.model.tile_map.tile_height

    def on_draw(self) -> None:
        self.camera.use()
        self.model.scene.draw()

    def on_update(self, delta_time: int) -> None:
        self._center_camera_to_player()

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Converts from screen coordinates to world coordinates."""
        return (
            self.camera.position.x + screen_x,
            self.camera.position.y + screen_y,
        )

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
