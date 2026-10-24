import random

def spawn_items(seed, game_map, start, count, taken=()):
    """Return `count` items on random floor cells not already used."""
    rng = random.Random(seed + 2)
    used = set(taken)
    candidates = [cell for cell in game_map.floor_cells() if cell not in used and cell != start]
    rng.shuffle(candidates)
    factories = [factory for factory, _ in ITEM_TABLE]
    weights = [weight for _, weight in ITEM_TABLE]
    return [rng.choices(factories, weights)[0](x, y) for x, y in candidates[:count]]
