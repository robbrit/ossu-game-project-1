from typing import (
    Protocol,
)

import engine
from engine import (
    controller,
    view,
)


class GUI(Protocol):
    @property
    def spec(self) -> "engine.gui.widgets.GUISpec":
        ...


class GameAPI(Protocol):
    def start_game(self) -> None:
        ...

    def show_gui(self, gui: GUI) -> None:
        ...


class GameState(Protocol):
    view: view.View
    controller: controller.Controller

    def setup(self, api: GameAPI) -> None:
        ...
