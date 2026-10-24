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
