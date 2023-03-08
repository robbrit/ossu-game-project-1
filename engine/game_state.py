from typing import (
    Protocol,
)

from engine import (
    controller,
    view,
)


class GUI(Protocol):
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
