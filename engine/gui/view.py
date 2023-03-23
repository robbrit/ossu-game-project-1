from typing import (
    List,
    Tuple,
)

import arcade

from engine import game_state


class GuiView:
    """
    Main view class. This manages rendering things to the screen.
    """

    gui: game_state.GUI
    sprites: arcade.SpriteList

    def __init__(self, initial_gui: game_state.GUI):
        self.gui = initial_gui
        self.sprites = arcade.SpriteList()
        self._load_sprites()

    def setup(self) -> None:
        # TODO(rob): Handle any setup.
        pass

    def on_draw(self) -> None:
        self.sprites.draw()

    def on_update(self, delta_time: int) -> None:
        pass

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        return screen_x, screen_y

    def set_gui(self, gui: game_state.GUI) -> None:
        self.gui = gui

    def _load_sprites(self) -> None:
        spec = self.gui.spec

        assets = {name: path for name, path in spec.assets}

        self.sprites = arcade.SpriteList()

        for button_spec in spec.buttons:
            # TODO(rob): Also load the selected image asset.
            button = arcade.Sprite(assets[button_spec.unselected_image_asset])
            button.center_x = button_spec.center[0]
            button.center_y = button_spec.center[1]
            self.sprites.append(button)

        # TODO(rob): Also handle images.
