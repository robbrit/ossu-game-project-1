import json

from engine import scripts
from engine.gui import widgets


class StartScreen:
    """Represents the start screen of the game."""

    spec: widgets.GUISpec

    def __init__(self):
        with open("assets/gui/start-screen.json") as f:
            data = json.loads(f.read())
            self.spec = widgets.GUISpec.create(data)


def start_game(api: scripts.GameAPI) -> None:
    api.start_game()
