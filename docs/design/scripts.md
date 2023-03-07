# Scripts

## In-Game

In-game scripts are custom code that happen based on a certain trigger.

- Owner - scripts can be tied to:
  - Items
  - Entities
  - Regions
- Triggers - event types that trigger the script
- State Variables:
  - Type (string, int, bool, reference)
  - Scope
    - Global - shared across all of a certain
    - Regional - specific to single region
    - Local - specific to a single script

### Events

- On start - when owner is first created
- On tick - every N milliseconds
- On collide - when entity collides with something
- On interact - when player interacts with entity
- On proximity - when another entity comes within a certain distance of owner
- On state change - whenever a state variable changes
- Custom - custom events can be defined and triggered by other scripts

### API

- FireEvent
- CreateEntity
- DestroyEntity
- MoveEntity
- GetVariable
- SetVariable
- ActivateGUI
- ChangeRegion

## GUI Scripts

When a GUI is activated, the game pauses and renders some GUI object. The GUI
object can use the API as any other script, but includes various buttons and
internal logic.

### Events

- Activate
- Cancel
- Move
