from typing import (
    Optional,
)

from arcade import gui

from engine import scripts


class GUI:
    """A base GUI that implements the GUI protocol."""

    api: Optional[scripts.GameAPI]
    manager: Optional[gui.UIManager]

    def __init__(self):
        self.api = None
        self.manager = None

    def set_api(self, api: scripts.GameAPI) -> None:
        """Sets the game API for this GUI."""
        self.api = api

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""
        self.manager = manager

        self.manager.clear()
        self._reset_widgets()

    def draw(self) -> None:
        """Renders the GUI."""

    def _reset_widgets(self) -> None:
        """Override to handle widget creation."""
