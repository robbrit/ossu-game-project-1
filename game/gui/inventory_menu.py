from typing import (
    Optional,
)

from arcade import gui

from engine import scripts


class InventoryMenu:
    """A GUI to handle the inventory."""

    api: Optional[scripts.GameAPI]
    manager: Optional[gui.UIManager]

    def __init__(self):
        self.api = None
        self.manager = None
        self.draw()

    def set_api(self, api: scripts.GameAPI) -> None:
        """Sets the game API for this GUI."""
        self.api = api

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""
        self.manager = manager

        self.manager.clear()

    def draw(self) -> None:
        """Renders the inventory menu."""

    def _resume_game(self, event: gui.UIOnClickEvent) -> None:
        # pylint: disable=unused-argument
        self.api.start_game()
