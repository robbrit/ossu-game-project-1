from typing import (
    Optional,
    Tuple,
)


from engine import (
    controller,
    scripts,
    view,
)
from engine.ingame import (
    controller as game_controller,
    view as game_view,
)
from engine.model import world


class InGameState:
    """Wraps the "in game" state."""

    game_world: world.World
    controller: controller.Controller
    view: view.View

    def __init__(
        self,
        game_world: world.World,
        viewport_size: Tuple[int, int],
        ingame_gui: Optional[scripts.GUI],
        menu_gui: scripts.GUI,
    ) -> None:
        self.game_world = game_world
        self.view = game_view.InGameView(game_world, viewport_size, gui=ingame_gui)
        self.controller = game_controller.InGameController(
            game_world,
            self.view,
            menu_gui,
        )

    def setup(self) -> None:
        """Sets up the in-game state."""
        self.view.setup()
        self.controller.setup()

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the game."""
        self.game_world.on_update(delta_time)
        self.view.on_update(delta_time)
        self.controller.on_update(delta_time)
