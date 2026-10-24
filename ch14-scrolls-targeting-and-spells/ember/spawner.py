# file: ember/spawner.py
"""Placing monsters on a freshly generated map."""
import random

from ember import entity_factories

MONSTER_TABLE = [   # (factory, relative weight)
    (entity_factories.rat, 4),
    (entity_factories.goblin, 6),
    (entity_factories.troll, 1),
    (entity_factories.imp, 2),
]


def spawn_monsters(seed, game_map, start, count, safe_radius=6):
    """Return `count` monsters on random floor cells away from the start."""
    rng = random.Random(seed + 1)          # a separate stream from the map's
    candidates = [(x, y) for (x, y) in game_map.floor_cells()
                  if max(abs(x - start[0]), abs(y - start[1])) > safe_radius]
    rng.shuffle(candidates)
    factories = [factory for factory, _ in MONSTER_TABLE]
    weights = [weight for _, weight in MONSTER_TABLE]
    monsters = []
    for x, y in candidates[:count]:
        factory = rng.choices(factories, weights)[0]
        monsters.append(factory(x, y))
    return monsters


ITEM_TABLE = [
    (entity_factories.health_potion, 70),
    (entity_factories.lightning_scroll, 10),
    (entity_factories.confusion_scroll, 10),
    (entity_factories.fireball_scroll, 10),
]


def spawn_items(seed, game_map, start, count, taken=()):
    """Return `count` items on random floor cells not already used."""
    rng = random.Random(seed + 2)
    used = set(taken)
    candidates = [cell for cell in game_map.floor_cells() if cell not in used and cell != start]
    rng.shuffle(candidates)
    factories = [factory for factory, _ in ITEM_TABLE]
    weights = [weight for _, weight in ITEM_TABLE]
    return [rng.choices(factories, weights)[0](x, y) for x, y in candidates[:count]]
