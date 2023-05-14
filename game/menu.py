from engine import scripts, core

from game.gui.inventory_menu import (
    InventoryMenu,
)


class Menu:
    """Handles methods related to the menu of this game."""

    _api: scripts.GameAPI
    inventory_menu: scripts.GUI

    def __init__(self, menu: InventoryMenu):
        self.inventory_menu = menu

    def show_menu(self):
        self.api.show_gui(self.inventory_menu)
        self.inventory_menu.draw()


def show_inventory(api: scripts.GameAPI = None):
    """Shows the inventory."""
    api.show_gui(InventoryMenu())
