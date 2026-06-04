# Wumpus — Code Skeleton

## Enums

- `Outcome` (Enum) — line 47

## Classes

### `Hazard`
- `__init__(self, kind, location, warning)`
  - `self.kind`
  - `self.location`
  - `self.warning`
- `encounter(self, player)`

### `Wumpus(Hazard)`
- `__init__(self, location, warning)`
  - `self.alive`
- `encounter(self, player)` # NO LONGER NEEDED - will be in encounter_handler()
  - calls `self.bumped()`
  - checks `self.location == player.location`
- `bumped(self)` # KEEP THIS - it's clean
  - reads `CAVE[self.location]`
  - sets `self.location`

### `Player`
- `__init__(self, location, arrows)`
  - `self.location`
  - `self.arrows`
  - `self.alive`
- `move(self, new_location, hazards)` # NO LONGER NEEDED since all functionality is moving elsewhere
  - sets `self.location`
  - iterates over `hazards` — checks `self.location == hazard.location` # MOVE TO AN encounter_handler() function
- `check_for_hit(self, room, target_location)` # MOVE TO module-level
- `shoot(self, path, wumpus_location)` # MOVE TO module-level
  - calls `self.check_for_hit()`
  - modifies `self.arrows`

## Module-level Functions

- `cave_setup()` — line 137
- `give_warnings(this_room, hazards)` — line 152
- `where_is_player(location)` — line 161
- `get_player_move()` — line 167
- `shoot_arrow(player, wumpus_location)` — line 178
- `move_player(player, hazards)` — line 199
- `main()` — line 213
