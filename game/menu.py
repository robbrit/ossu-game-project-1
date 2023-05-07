from engine import (
    scripts,
)

from gui import (
    inventory_menu,
)


class Menu:
    """Handles methods related to the menu of this game."""

    _api: scripts.GameAPI
    _inventory_menu: scripts.GUI

    def show_inventory(self, api: scripts.GameAPI):
        """Shows the inventory."""
        api.show_gui(inventory_menu.InventoryMenu())
