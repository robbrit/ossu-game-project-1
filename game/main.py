import json

from engine import (
    core,
    spec,
)
from game.gui import start


def run() -> None:
    """Runs the game."""
    with open("assets/game-spec.json") as infile:
        data = json.loads(infile.read())
        game_spec = spec.GameSpec(**data)

    core.Core(
        initial_gui=start.StartScreen(),
        game_spec=game_spec,
    ).run()
