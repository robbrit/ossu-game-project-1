import enum
from typing import (
    List,
    Protocol,
    Tuple,
)

from pyglet import math as pmath

from engine import scripts


class NavigatorState(enum.Enum):
    """Represents the state of the waypoint navigator."""

    MOVING = 1
    IDLING = 2


DEFAULT_IDLE_SECS = 5
DEFAULT_PROXIMITY = 5
DEFAULT_SPEED = 80


class NavigatorOwner(Protocol):
    """A protocol defining what methods are necessary to be an owner of a navigator."""

    @property
    def speed(self) -> Tuple[float, float]:
        """Gets the speed of the owner."""

    @speed.setter
    def speed(self, value: Tuple[float, float]) -> None:
        """Sets the speed of the owner."""

    @property
    def location(self) -> Tuple[float, float]:
        """Gets the location of the owner."""


class Navigator:
    """Class that handles state tracking for waypoints."""

    _waypoints: List[scripts.KeyPoint]
    _current_waypoint_idx: int
    _last_transition_time: float
    _state: NavigatorState
    _owner: NavigatorOwner
    _idle_secs: float
    _proximity: float
    _speed: float

    def __init__(
        self,
        owner: NavigatorOwner,
        waypoints: List[scripts.KeyPoint],
        idle_secs: float = DEFAULT_IDLE_SECS,
        proximity: float = DEFAULT_PROXIMITY,
        speed: float = DEFAULT_SPEED,
    ):
        """Constructs a new wanderer."""
        self._waypoints = waypoints
        self._current_waypoint_idx = -1
        self._last_transition_time = 0.0
        self._state = NavigatorState.IDLING
        self._owner = owner
        self._idle_secs = idle_secs
        self._proximity = proximity
        self._speed = speed

    def on_tick(self, game_time: float) -> None:
        """Handles tick events."""
        if self._state == NavigatorState.IDLING:
            self._handle_idle(game_time)
        elif self._state == NavigatorState.MOVING:
            self._handle_moving(game_time)

    def _handle_idle(self, game_time: float) -> None:
        if game_time < self._last_transition_time + self._idle_secs:
            return

        # Alright, time to move on.
        next_waypoint_idx = (self._current_waypoint_idx + 1) % len(self._waypoints)
        self._current_waypoint_idx = next_waypoint_idx

        delta = self._vec_to_waypoint(next_waypoint_idx).normalize().scale(self._speed)
        self._owner.speed = (delta.x, delta.y)
        self._state = NavigatorState.MOVING

    def _handle_moving(self, game_time: float) -> None:
        distance = self._vec_to_waypoint(self._current_waypoint_idx).mag

        if distance > self._proximity:
            return

        # We're close enough to the waypoint, stop here.
        self._owner.speed = (0, 0)
        self._state = NavigatorState.IDLING
        self._last_transition_time = game_time

    def _vec_to_waypoint(self, waypoint_idx) -> pmath.Vec2:
        x, y = self._owner.location
        next_waypoint = self._waypoints[waypoint_idx]
        target_x, target_y = next_waypoint.location

        return pmath.Vec2(target_x - x, target_y - y)
