# Player

## State

Properties:

- State (enum)
- Equipped (see below)
- Inventory (see below)
- Journal (see below)

### Player State

- Alive - can move around, all collisions apply
- Invincible - same as alive but cannot take damage
- Dead - cannot move around, invisible to monsters

## Equipped

Set of slots:

- Slot name (string)
- Current item (item)
- Allowed item types (enum[])

## Inventory

Contains a list of items:

- Name
- Item Type
- Quantity

### Item Type

Properties:

- Default name (string)
- Stack size (int)
- Item class (enum)
  - Weapon, armor, other

## Journal

- Places discovered
- State of all quests
