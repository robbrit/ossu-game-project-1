from typing import (
    Any,
    Callable,
    Dict,
    Optional,
)

import arcade
from arcade import gui

from engine import scripts
from engine.gui import widgets


class SpecGUI:
    """A GUI class that draws itself based on a spec."""

    sprites: arcade.SpriteList
    manager: Optional[gui.UIManager]
    api: scripts.GameAPI
    textures: Dict[str, arcade.Texture]

    def __init__(self, api: scripts.GameAPI, spec: widgets.GUISpec):
        self.api = api
        self.spec = spec
        self.sprites = arcade.SpriteList()
        self.manager = None
        self.textures = {}
        self._load_textures()

    def draw(self) -> None:
        """Draws the GUI."""
        self.sprites.draw()

    def set_api(self, api: scripts.GameAPI):
        """Sets the game API for this GUI."""
        self.api = api

    def set_manager(self, manager: gui.UIManager):
        """Sets the UI manager for this GUI."""
        self.manager = manager
        self.manager.clear()
        self._build_widgets(manager)

    def _build_widgets(self, manager: gui.UIManager) -> None:
        for button_spec in self.spec.buttons:

            def _on_click(
                action: scripts.GameCallable,
            ) -> Callable[[gui.UIOnClickEvent], Any]:
                return lambda unused: action(self.api)

            button = gui.UITextureButton(
                texture=self.textures[button_spec.unselected_image_asset],
                x=button_spec.center[0],
                y=button_spec.center[1],
            )
            button.on_click = _on_click(button_spec.action)  # type: ignore
            manager.add(button, index=0)

    def _load_textures(self) -> None:
        self.textures = {}
        self.sprites = arcade.SpriteList()

        for asset in self.spec.assets:
            self.textures[asset.name] = arcade.load_texture(asset.path)

        for image_spec in self.spec.images:
            image = arcade.Sprite(texture=self.textures[image_spec.image_asset])
            image.center_x = image_spec.center[0]
            image.center_y = image_spec.center[1]
            self.sprites.append(image)
