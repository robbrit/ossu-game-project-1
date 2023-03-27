import importlib
from typing import Callable

from engine import game_state


GameCallable = Callable[[game_state.GameAPI], None]


def load_callable(path: str) -> GameCallable:
    """Loads a callable object.

    Note that this doesn't actually check if the thing is callable, or checks the
    arguments/return type.
    """
    mod_name, class_name = path.rsplit(".", 1)

    # TODO(rob): Determine if this is insecure.
    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)
