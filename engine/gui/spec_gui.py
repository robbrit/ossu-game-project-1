from typing import Iterable

import arcade
from arcade import gui

from engine import scripts
from engine.gui import widgets


class SpecGUI:
    """A GUI class that draws itself based on a spec."""

    sprites: arcade.SpriteList

    def __init__(self, spec: widgets.GUISpec):
        self.spec = spec
        self.sprites = arcade.SpriteList()
        self._load_sprites()

    def draw(self) -> None:
        self.sprites.draw()

    def set_api(self, api: scripts.GameAPI):
        pass

    def set_manager(self, manager: gui.UIManager):
        pass

    def _load_sprites(self) -> None:
        assets = dict(self.spec.assets)

        self.sprites = arcade.SpriteList()

        for button_spec in self.spec.buttons:
            # TODO(rob): Also load the selected image asset.
            button = arcade.Sprite(assets[button_spec.unselected_image_asset])
            button.center_x = button_spec.center[0]
            button.center_y = button_spec.center[1]
            self.sprites.append(button)

        for image_spec in self.spec.images:
            image = arcade.Sprite(assets[image_spec.image_asset])
            image.center_x = image_spec.center[0]
            image.center_y = image_spec.center[1]
            self.sprites.append(image)
