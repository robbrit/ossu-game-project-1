# Controller

## Game State

### In GUI

A GUI is specified by:

Some named tuples:

- `Button` - something that can be interacted with by the user
  - Unselected image - resource name to render when the button is not selected
  - Selected image - resource name to render when the button is selected
  - Name - the name of the button. Must be unique within the GUI
  - Left/Right/Up/Down buttons - optional strings referencing other buttons
  - Center position - (x, y) coordinates on the screen
  - Action - function to call when the A button is pushed when this button is
    selected
- `Label` - some basic text
  - Text - the text to show
  - Center position - (x, y) coordinates on the screen
- `Image` - a basic image
  - Image - resource name to render
  - Center position
- Selected button - string referencing the button that is currently selected.
- Cancel action - function to call when the B button is pushed.

The view:

- will render all buttons, labels, and images according to their center
  positions.
- will render the selected button using the selected image

The controller:

- will translate directional motions into left/right/up/down. If the selected
  button has a button in that direction, switches the selected button.
  - movement and facing directions both do the same thing, it doesn't matter
    which one the user chooses
- will execute the selected button's action when the A button is pressed
- will execute the GUI's cancel action when the B button is pressed

### Playing

World update loop advances as normal.

Controls:

- Directional updates the player velocity, applying any collisions.
- A causes an interaction with any entity in front of the player.
- B, C, D, L, R triggers a script on whatever items are bound to those slots.
- Start pauses the game.

## Input Format

Translates from the actual input to a set of well-defined controls.

## Controls

- Movement (360 degrees)
- Facing (360 degrees)
- Active buttons (A, B, C, D, L, R)
- 1 Control button (Start)
