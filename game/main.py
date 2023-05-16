import json

from engine import (
    core,
    scripts,
    spec,
)
from engine.gui import spec_gui
from game.gui import (
    hud,
)
from game.scripts import health

STARTING_HP = 10
STARTING_GOLD = 50
STARTING_DAMAGE = 4


def run() -> None:
    """Runs the game."""
    with open("assets/game-spec.json") as infile:
        data = json.loads(infile.read())
        game_spec = spec.GameSpec(**data)

    def create_start_screen(api: scripts.GameAPI) -> scripts.GUI:
        return spec_gui.SpecGUI(api, game_spec.guis["start-screen"])

    def create_hud(api: scripts.GameAPI) -> scripts.GUI:
        return hud.HUD(api)

    def create_menu_gui(api: scripts.GameAPI) -> scripts.GUI:
        return spec_gui.SpecGUI(api, game_spec.guis["ingame-menu"])

    core.Core(
        initial_gui=create_start_screen,
        ingame_gui=create_hud,
        menu_gui=create_menu_gui,
        game_spec=game_spec,
        initial_player_state={
            "hp": health.Health(STARTING_HP),
            "gold": STARTING_GOLD,
            "base_damage": STARTING_DAMAGE,
            "last_damage_time": 0.0,
            "quests": {},
        },
    ).run()
