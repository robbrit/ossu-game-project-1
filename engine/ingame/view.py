from typing import (
    Optional,
    Tuple,
)

from pyglet import math as pmath

import arcade
import arcade.tilemap

from engine import (
    scripts,
)
from engine.model import world


class InGameView:
    """
    Renders the world while the user is in the game.
    """

    game_world: world.World
    camera: arcade.Camera
    gui: Optional[scripts.GUI]
    gui_camera: arcade.Camera

    def __init__(
        self,
        game_world: world.World,
        viewport_size: Tuple[int, int],
        gui: Optional[scripts.GUI],
    ):
        self.game_world = game_world
        self.gui = gui
        self.camera = arcade.Camera(
            viewport_size[0],
            viewport_size[1],
        )
        self.gui_camera = arcade.Camera(
            viewport_size[0],
            viewport_size[1],
        )

    @property
    def world_width(self) -> int:
        """Returns the width of the world."""
        return self.game_world.width * self.game_world.tile_width

    @property
    def world_height(self) -> int:
        """Returns the height of the world."""
        return self.game_world.height * self.game_world.tile_height

    def setup(self) -> None:
        """Sets up the view."""

    def on_draw(self) -> None:
        """Renders the view."""
        self.camera.use()
        self.game_world.draw()

        if self.gui is not None:
            self.gui_camera.use()
            self.gui.draw()

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the view."""
        # pylint: disable=unused-argument
        self._center_camera_to_player()

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Converts from screen coordinates to world coordinates."""
        return (
            self.camera.position.x + screen_x,
            self.camera.position.y + screen_y,
        )

    def _center_camera_to_player(self) -> None:
        player = self.game_world.player_sprite

        v_width = self.camera.viewport_width
        v_height = self.camera.viewport_height

        if self.world_width < v_width:
            camera_x = (self.world_width - v_width) / 2
        else:
            camera_x = min(
                self.world_width - v_width,
                max(
                    0,
                    player.center_x - v_width / 2,
                ),
            )

        if self.world_height < v_height:
            camera_y = (self.world_height - v_height) / 2
        else:
            camera_y = min(
                self.world_height - v_height,
                max(
                    0,
                    player.center_y - v_height / 2,
                ),
            )

        self.camera.move_to(pmath.Vec2(camera_x, camera_y))
