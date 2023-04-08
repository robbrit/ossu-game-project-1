import json

from engine import (
    core,
    scripts,
    spec,
)
from game.gui import start

STARTING_HP = 10


def run() -> None:
    """Runs the game."""
    with open("assets/game-spec.json") as infile:
        data = json.loads(infile.read())
        game_spec = spec.GameSpec(**data)

    def create_start_screen(api: scripts.GameAPI) -> scripts.GUI:
        return start.StartScreen(api)

    core.Core(
        initial_gui=create_start_screen,
        game_spec=game_spec,
        initial_player_state={
            "hp": 10,
        },
    ).run()
