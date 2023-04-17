import json

from engine import (
    core,
    scripts,
    spec,
)
from game.gui import (
    hud,
    start,
)

STARTING_HP = 10


def run() -> None:
    """Runs the game."""
    with open("assets/game-spec.json") as infile:
        data = json.loads(infile.read())
        game_spec = spec.GameSpec(**data)

    def create_start_screen(api: scripts.GameAPI) -> scripts.GUI:
        return start.StartScreen(api)

    def create_hud(api: scripts.GameAPI) -> scripts.GUI:
        return hud.HUD(api)

    core.Core(
        initial_gui=create_start_screen,
        ingame_gui=create_hud,
        game_spec=game_spec,
        initial_player_state={
            "hp": STARTING_HP,
            "max_hp": STARTING_HP,
        },
    ).run()
