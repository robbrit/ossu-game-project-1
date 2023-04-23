# Scripts

## Scripted Objects

Scripted objects are defined in the Tiled map editor output. These are elements
of the region that will have some sort of logic that is executed.

Scripted objects can define their behaviour in two ways:

- Using the `script` custom property. This is the name of a class that inherits
  from the `engine.scripts.Script` class.
  - The constructor of the class may contain arguments, which will be populated
    based on any custom properties as defined below.
- Using the `on_*` custom properties, matching any of the `on_*` methods defined
  by the `engine.scripts.Script` class. These are for when very simple logic is
  needed by the scripted object, and entire class is not necessary.
  - The value of the property must be the name of a function.
  - The function accepts arguments that may be defined as below. Note that these
    arguments are not the same as the ones passed to a `Script` object.
  - Multiple `on_*` properties may be provided.
  - These simple properties do not retain any state, if you want something that
    can retain state you'll need to use a class.

### Arguments

Arguments are passed in the form `<prefix>_<argument name>`. The `prefix` can be
either `script_` for scripts using the `script` custom property, or `on_*_` for
function-based triggers. The `argument name`

For example, a scripted object in region "Forest" that triggers a transition to
region "My Town" when something collides with it would have three custom
properties:

- `on_collide`: `engine.builtin.transition_region`
- `on_collide_region`: `My Town`
- `on_collide_start_location`: `Entry from Forest`

### Built-Ins

A set of built-in scripts are defined in `engine.builtin`. These are commonly
used functionality such as region transitions. See the docs on the objects in
that module for more details.
