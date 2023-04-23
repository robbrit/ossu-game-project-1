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

The game is separated into two major areas: the engine and the game logic. The
engine handles code that is relatively independent of the gameplay of the game
such as user input, rendering, collisions, etc.

The game logic layer handles code specific to this game: enemy behaviour,
internal GUIs, etc.

### Engine

#### Overall Architecture

The engine roughly follows an MVC (model-view-controller) architecture. Models
capture the state of the world in the game: players, monsters, towns, etc. The
view handles any sort of rendering, and the controller handles any sort of user
interaction.

There is only one model, but views and controllers are paired together in a
"game state" object. This allows the game logic to transition the game between
different states that will have different display and control schemes.

The game can be in one of a set number of states:

- In GUI
- Playing

When the state is in GUI, the model update loop will not be called, but objects
can still be modified.

An edge case is when the game is first loaded and the model state doesn't exist
yet. Because of this the model passed to views/controllers is `Optional`, they
will need to handle this edge case.

More details:

- [Model Design](model.md)
- [View-Controller Design](view-controller.md)

### Game Logic

Game logic is captured in several ways:

- The core game wrapper: the game defines its own main entry point, and
  instantiates an `engine.core.Core` object to start the game.
- GUIs: the game defines various GUIs that adhere to the `GUI` interface. These
  are separate screens, and are the primary way for a game to customize view and
  controller logic.
- Scripts: the game defines scripts that adhere to the `Script` interface. These
  live within the game, and are the primary way for a game to customize model
  logic.

The engine provides ways for GUIs and scripts to interact with it in several
ways:

- The game interface (`engine.scripts.GameAPI`) - this is an interface that is
  passed to scripts, that they can use as they will.
- The script interface (`engine.scripts.Script`) - a script can override any of
  the methods on the base script class to have custom functionality trigger on
  various events (collisions, player activating it, etc.).
- Static data files - these are files loaded by the engine, which can reference
  script/GUI code by name.

#### Spec Files

At a high level, static data for the game is captured by a JSON spec file that
adheres to the `engine.spec.GameSpec` structure. This spec is loaded by the core
game engine and contains a number of configuration options.

#### Tiled Map Files

The engine uses the [Tiled Map Editor](https://www.mapeditor.org/) to represent
its maps. While much of the content is static, the engine allows objects to
contain custom properties that reference code. The [model docs](model.md) will
describe this in more detail.
