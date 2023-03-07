# Model Design

Key Object Types:

- Regions
- Entities
- Game State

## Regions

A region contains the tile layout, and zones.

### Tiles

- Use Tiled format.
- 32x32 pixels for a tile.

### Initial Entities

List of entities in the zone when the zone is first loaded. Only happens in the
first load of the region, later loads will simply reload the game state.

### Zones

Named zones, cover a certain subset of the region.

## Scripts

See [scripts](scripts.md).

## Entities

All entities have the following properties:

- Position (x, y)
- Orientation (enum)
- Sprite (sprite)
- State Variables (any)

### Player

See [player docs](player.md).

### NPCs

Properties:

- Creature Type (enum)
- Behavior override (script)

#### Creature Types

Properties:

- Behavior (script)

### Doodads

Properties:

- Doodad Type (enum)
- Solid (bool)

## Persistence

Storage:

- Region state
  - Non-player entity states
- Player state
- Script states
