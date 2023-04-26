import enum
from typing import (
    List,
)

from pyglet import math as pmath

from engine import scripts


class RatState(enum.Enum):
    """Represents the state of the rat."""

    MOVING = 1
    IDLING = 2


RAT_IDLE_SECS = 5
RAT_SPEED = 2
RAT_PROXIMITY = 5


class Rat(scripts.SavesAPI, scripts.SavesOwner, scripts.Script):
    """A rat creature."""

    waypoint_names: List[str]
    waypoints: List[scripts.KeyPoint]
    current_waypoint_idx: int
    last_transition_time: float
    state: RatState

    def __init__(self, **kwargs):
        """Constructs a new rat.

        Expected kwargs:
          waypoint_N - The names of waypoints that the rat will wander between.
                       The actual values of N don't matter, so long as they are
                       unique.
        """
        # TODO(rob): The wandering logic can probably be put into a class.
        waypoint_args = [
            int(index)
            for index in scripts.extract_script_args("waypoint_", kwargs).keys()
        ]
        self.waypoint_names = [kwargs[f"waypoint_{n}"] for n in waypoint_args]
        self.waypoints = []
        self.current_waypoint_idx = -1
        self.last_transition_time = 0.0
        self.state = RatState.IDLING

    def set_api(self, api: scripts.GameAPI) -> None:
        """Sets the API for the rat."""
        super().set_api(api)
        self.waypoints = [api.get_key_points(name)[0] for name in self.waypoint_names]

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Handles game ticks."""

        if self.state == RatState.IDLING:
            self._handle_idle(game_time)
        elif self.state == RatState.MOVING:
            self._handle_moving(game_time)

    def _handle_idle(self, game_time: float) -> None:
        if game_time < self.last_transition_time + RAT_IDLE_SECS:
            return

        # Alright, time to move on.
        next_waypoint_idx = (self.current_waypoint_idx + 1) % len(self.waypoints)
        self.current_waypoint_idx = next_waypoint_idx

        delta = self._vec_to_waypoint(next_waypoint_idx).normalize().scale(RAT_SPEED)
        self.owner.speed = (delta.x, delta.y)
        self.owner.facing = (delta.x, delta.y)
        self.state = RatState.MOVING

    def _handle_moving(self, game_time: float) -> None:
        distance = self._vec_to_waypoint(self.current_waypoint_idx).mag

        if distance > RAT_PROXIMITY:
            return

        # We're close enough to the waypoint, stop here.
        self.owner.speed = (0, 0)
        self.state = RatState.IDLING
        self.last_transition_time = game_time

    def _vec_to_waypoint(self, waypoint_idx) -> float:
        x, y = self.owner.location
        next_waypoint = self.waypoints[waypoint_idx]
        target_x, target_y = next_waypoint.location

        return pmath.Vec2(target_x - x, target_y - y)
