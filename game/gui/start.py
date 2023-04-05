import json

from engine import (
    core,
    scripts,
)
from engine.gui import (
    spec_gui,
    widgets,
)


class StartScreen(spec_gui.SpecGUI):
    """Represents the start screen of the game."""

    def __init__(self):
        with open("assets/gui/start-screen.json") as infile:
            data = json.loads(infile.read())
            spec = widgets.GUISpec.create(data, (core.SCREEN_WIDTH, core.SCREEN_HEIGHT))
            super().__init__(spec)


def start_game(api: scripts.GameAPI) -> None:
    """Starts the game."""
    api.start_game()
