import random

def populate(seed, depth, game_map, start, avoid=()):
    """Return the monsters and items for one floor, placed on free cells."""
    rng = random.Random(seed * 31 + depth)
    blocked = set(avoid) | {start}
    def far_enough(cell):
        return max(abs(cell[0] - start[0]), abs(cell[1] - start[1])) > 5

    candidates = [cell for cell in game_map.floor_cells()
                  if cell not in blocked and far_enough(cell)]
    rng.shuffle(candidates)

    entities = []
    monster_types, monster_weights = table_for_depth(MONSTER_CHANCES, depth)
    item_types, item_weights = table_for_depth(ITEM_CHANCES, depth)
    n_monsters = amount_for_depth(MONSTERS_PER_FLOOR, depth)
    n_items = amount_for_depth(ITEMS_PER_FLOOR, depth)
    for x, y in candidates[:n_items]:
        entities.append(rng.choices(item_types, item_weights)[0](x, y))
    for x, y in candidates[n_items:n_items + n_monsters]:
        entities.append(rng.choices(monster_types, monster_weights)[0](x, y))
    return entities
