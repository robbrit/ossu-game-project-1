# Controller

## Game State

### Out-game GUI

Controls:

- Directional moves the currently selected GUI item.
- A activates the currently selected GUI item.
- B triggers a Cancel event.
- Other buttons don't do anything.

### In-game GUI

GUIs are customizeable, so inputs are just sent as-is to the GUI object.

### Playing

World update loop advances as normal.

Controls:

- Directional updates the player velocity, applying any collisions.
- A causes an interaction with any entity in front of the player.
- B, C, D, L, R triggers a script on whatever items are bound to those slots.
- Start pauses the game.

### Paused

World update loop does not advance.

Renders a paused GUI, if any.

## Input Format

Translates from the actual input to a set of well-defined controls.

## Controls

- Directional (8 directions)
- Active buttons (A, B, C, D, L, R)
- 1 Control button (Start)
