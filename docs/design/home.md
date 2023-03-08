# Design Doc

## Vision

Key ideas:

- Fantasy-style RPG
  - Fight monsters
  - Do quests
- Open world
  - Can go anywhere in the world, monsters scale up with the player
- Top-Down 2D Pixel Graphics

Exclusions:

- Multiplayer
- 3D Graphics
- Mobile/Web

## Design

### Engine

#### MVC Architecture

- [Model Design](model.md)
- [View Design](view.md)
- [Controller Design](controller.md)

#### Game State

The game can be in one of a set number of states:

- In GUI
- Playing

With the MVC architecture, the model layer will remain the same regardless of
what the state is but the views and controllers will change. They will adhere
to a common interface, but different classes can be specified.

When the state is in GUI, the model update loop will not be called, but objects
can still be modified.

An edge case is when the game is first loaded and the model state doesn't exist
yet. Because of this the model passed to views/controllers is `Optional`, they
will need to handle this edge case.
