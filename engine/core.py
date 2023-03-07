from typing import Optional

import arcade
import arcade.tilemap

from engine import (
    controller,
    model,
    view,
)


class Core(arcade.Window):
    """
    Main application class.
    """

    game_view: view.View
    model: model.Model
    controller: controller.Controller

    def __init__(self):
        super().__init__(
            view.SCREEN_WIDTH,
            view.SCREEN_HEIGHT,
            view.SCREEN_TITLE,
        )

        self.model = model.Model()
        self.controller = controller.Controller(self.model)
        self.game_view = view.View(self.model)

    def setup(self) -> None:
        self.model.setup()
        self.game_view.setup((self.width, self.height))

    def on_draw(self) -> None:
        self.clear()
        self.game_view.on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.controller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.controller.on_key_release(symbol, modifiers)

    def on_update(self, delta_time: int) -> None:
        self.model.on_update(delta_time)
        self.controller.on_update(delta_time)
        self.game_view.on_update(delta_time)

    def run(self):
        self.setup()
        arcade.run()
