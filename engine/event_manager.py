import collections
from typing import (
    Any,
    Dict,
    List,
)

from engine import scripts


class EventManager:
    """Class that manages any sort of event processing."""

    _handlers: Dict[str, List[scripts.EventHandler]]

    def __init__(self):
        self._handlers = collections.defaultdict(list)

    def register_handler(self, event_name: str, handler: scripts.EventHandler) -> None:
        """Registers an event handler for a custom event."""
        self._handlers[event_name].append(handler)

    def unregister_handler(
        self,
        event_name: str,
        handler: scripts.EventHandler,
    ) -> None:
        """Unregisters an event handler."""
        self._handlers[event_name] = [
            _handler for _handler in self._handlers[event_name] if _handler != handler
        ]

    def fire_event(self, event_name: str, data: Any) -> None:
        """Fires an event."""
        for handler in self._handlers[event_name]:
            handler(event_name, data)
