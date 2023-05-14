from typing import (
    Optional,
)

from arcade import gui

from engine import scripts

from game.equipment import (
    inventory,
)


CONVERSATION_PADDING = 10
CONVERSATION_Y = 200
CONVERSATION_HEIGHT = 180
SCREEN_HEIGHT = 600
CHOICES_OFFSET = 650
CHOICE_HEIGHT = 30


class _InventorySlot(gui.UIFlatButton):
    """Class to allow us to attach data to a UI Button."""

    index: int

    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index


class InventoryMenu:
    """A GUI to handle the inventory."""

    _inventory: inventory.Inventory
    api: Optional[scripts.GameAPI]
    manager: Optional[gui.UIManager]

    def __init__(self):
        self.api = None
        self.manager = None
        self._inventory = inventory.Inventory()

    def set_api(self, api: scripts.GameAPI) -> None:
        """Sets the game API for this GUI."""
        self.api = api

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""
        self.manager = manager

        self.manager.clear()

    def draw(self) -> None:
        """Renders the inventory menu."""
        self.manager.clear()
        # Dirty hack to get the UI manager to reset correctly.
        self.manager.children[0] = []

        self.manager.add(
            gui.UITextArea(
                x=CONVERSATION_PADDING,
                y=CONVERSATION_Y,
                height=CONVERSATION_HEIGHT,
                text="TEST",
            ),
            index=0,
        )

        for i, choice in enumerate(self._inventory.get_items()):
            button = _InventorySlot(
                index=i,
                x=CHOICES_OFFSET,
                y=(i + 1) * CHOICE_HEIGHT + CONVERSATION_PADDING,
                height=CHOICE_HEIGHT,
                text=f"test {i}",
            )
            # button.on_click = self._choice_picked
            self.manager.add(button, index=0)

        exit_button = gui.UIFlatButton(
            x=CHOICES_OFFSET,
            y=CONVERSATION_PADDING,
            height=CHOICE_HEIGHT,
            text="Exit",
        )
        exit_button.on_click = self._resume_game
        self.manager.add(exit_button, index=0)

        title = "TESTING THIS OUT"
        if title is not None:
            self.manager.add(
                gui.UILabel(
                    x=CONVERSATION_PADDING,
                    y=SCREEN_HEIGHT - CONVERSATION_PADDING,
                    text=title,
                    bold=True,
                ),
                index=0,
            )

    def _resume_game(self, event: gui.UIOnClickEvent) -> None:
        # pylint: disable=unused-argument
        self.api.start_game()
