# Model Design

The model combines together the state of the world. Regions, scripts, game
objects are all captured in this layer.

Right now the code contains an object called "World", which is synonymous with
"Model". This will change later, the model will be the top-level piece and will
wrap multiple objects, including the world.

## Regions

A region contains the tile layout, and zones. It is defined purely by the Tiled
map editor's output in JSON format.

Some details on the maps:

- They use 32x32 pixels for tiles.
- Solid terrain is in a tile layer called "Wall Tiles". Any occupied space in
  this layer is impassable.
- An optional object layer named "Scripted Objects" can contain a set of objects
  that bind to some sort of scriptable logic. See the
  [scripts docs](scripts.md#scripted-objects) for more details.
- A required "Key Points" layer contains a set of entrypoints to the region that
  can be referenced by other scripts.

## Scripts

See [scripts](scripts.md).
