# file: ember/spawner.py
"""Placing monsters and items on a freshly generated floor.

What appears, and how much of it, depends on how deep the floor is.
"""
import random

from ember import entity_factories

# For each table: from this depth onward, these (factory, weight) pairs
# apply. A later entry for the same factory replaces the earlier weight.
MONSTER_CHANCES = {
    1: [(entity_factories.rat, 40), (entity_factories.goblin, 60)],
    2: [(entity_factories.imp, 15)],
    3: [(entity_factories.troll, 10)],
    5: [(entity_factories.troll, 25), (entity_factories.rat, 20)],
    7: [(entity_factories.troll, 45), (entity_factories.imp, 25)],
}
ITEM_CHANCES = {
    1: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}
# (from depth, how many) — the last matching row wins.
MONSTERS_PER_FLOOR = [(1, 6), (3, 9), (5, 12), (8, 15)]
ITEMS_PER_FLOOR = [(1, 3), (4, 5), (7, 6)]


def table_for_depth(chances, depth):
    weights = {}
    for start_depth in sorted(chances):
        if start_depth > depth:
            break
        for factory, weight in chances[start_depth]:
            weights[factory] = weight
    return list(weights), list(weights.values())


def amount_for_depth(rows, depth):
    amount = 0
    for start_depth, value in rows:
        if start_depth <= depth:
            amount = value
    return amount


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
