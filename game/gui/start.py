import json

from engine import scripts
from engine.gui import (
    spec_gui,
    widgets,
)


class StartScreen(spec_gui.SpecGUI):
    """Represents the start screen of the game."""

    def __init__(self):
        with open("assets/gui/start-screen.json") as f:
            data = json.loads(f.read())
            spec = widgets.GUISpec.create(data)
            super().__init__(spec)


def start_game(api: scripts.GameAPI) -> None:
    api.start_game()
