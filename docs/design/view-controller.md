# View Controller Design

Views and controllers in the game are fairly tightly-coupled.

## Game State

A "game state" wraps a view-controller pair. This object manages feeding calls
from the Arcade subsystem into the respective classes.

There are two primary states: "GUI" and "In-Game".

### GUI States

GUI states are fairly simple classes wrapping a `GUI` object. These are designed
to be managed mainly by Arcade's GUI system.

### In-Game States

#### Controller

The in-game view uses the mouse and keyboard to navigate. These control the
character:

- Mouse controls the direction the player is facing.
- Arrow keys or WASD control the direction the player is moving.
- The left mouse button triggers an "activate" call.

#### View

The view renders two pieces:

- The world, based on a camera centered on the player.
- Any in-game GUI passed to the `Core` object.
