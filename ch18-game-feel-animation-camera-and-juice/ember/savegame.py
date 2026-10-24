# file: ember/savegame.py
"""Saving and loading a run as JSON.

We save *data*, not Python objects: for every entity we record which
factory built it plus whatever has changed since (position, hit points,
inventory and so on). Loading calls the same factory again and then
applies the saved changes. That keeps the save file small, readable and
safe to load, and old saves keep working when we tweak a monster's
colour.
"""
import json
from pathlib import Path

from ember import ai, entity_factories, game_world, tiles
from ember.engine import Engine
from ember.game_map import GameMap

SAVE_PATH = Path.home() / ".ember-depths" / "savegame.json"
SAVE_VERSION = 1

# Every factory, keyed by the name of the entity it builds.
FACTORIES = [entity_factories.player, entity_factories.rat, entity_factories.goblin,
             entity_factories.troll, entity_factories.imp, entity_factories.health_potion,
             entity_factories.lightning_scroll, entity_factories.confusion_scroll,
             entity_factories.fireball_scroll, entity_factories.dagger, entity_factories.sword,
             entity_factories.leather_armor, entity_factories.chain_mail, game_world.ember_crown]
FACTORY_BY_NAME = {factory(0, 0).name: factory for factory in FACTORIES}
TILE_BY_NAME = {tile.name: tile for tile in (tiles.FLOOR, tiles.WALL, tiles.DOWN_STAIRS)}
CORPSE_PREFIX = "remains of "


# -------- saving
def ai_to_dict(brain):
    if brain is None:
        return None
    data = {"type": type(brain).__name__}
    if isinstance(brain, ai.HostileEnemy):
        data["last_seen"] = brain.last_seen
    elif isinstance(brain, ai.ConfusedEnemy):
        data["turns"] = brain.turns_remaining
        data["previous"] = ai_to_dict(brain.previous_ai)
    return data


def entity_to_dict(entity):
    data = {"name": entity.name, "x": entity.x, "y": entity.y, "energy": entity.energy,
            "ai": ai_to_dict(entity.ai)}
    if entity.fighter:
        f = entity.fighter
        data["fighter"] = {"hp": f.hp, "max_hp": f.max_hp,
                           "base_power": f.base_power, "base_defense": f.base_defense}
    if entity.level:
        lv = entity.level
        data["level"] = {"current_level": lv.current_level, "current_xp": lv.current_xp}
    if entity.inventory:
        data["inventory"] = [entity_to_dict(item) for item in entity.inventory.items]
    if entity.equipment:
        items = entity.inventory.items
        data["equipped"] = [items.index(item) for item in entity.equipment.slots.values() if item]
    return data


def save_game(engine, path=SAVE_PATH):
    gm = engine.game_map
    data = {
        "version": SAVE_VERSION,
        "seed": engine.game_world.seed,
        "depth": engine.game_world.depth,
        "turn": engine.turn,
        "map": {"width": gm.width, "height": gm.height,
                "tiles": [[gm.tiles[x][y].name for y in range(gm.height)] for x in range(gm.width)],
                "explored": sorted(gm.explored)},
        "player_index": engine.entities.index(engine.player),
        "entities": [entity_to_dict(e) for e in engine.entities],
        "messages": [[m.plain_text, list(m.color), m.count] for m in engine.message_log.messages[-100:]],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data))
    temp.replace(path)     # write-then-rename: a crash can't leave half a save


def delete_save(path=SAVE_PATH):
    if path.exists():
        path.unlink()


# -------- loading
def ai_from_dict(data, entity):
    if data is None:
        return None
    brain_class = getattr(ai, data["type"])
    if brain_class is ai.ConfusedEnemy:
        return ai.ConfusedEnemy(entity, ai_from_dict(data["previous"], entity), data["turns"])
    brain = brain_class(entity)
    if "last_seen" in data and data["last_seen"] is not None:
        brain.last_seen = tuple(data["last_seen"])
    return brain


def entity_from_dict(data):
    name = data["name"]
    is_corpse = name.startswith(CORPSE_PREFIX)
    factory = FACTORY_BY_NAME[name[len(CORPSE_PREFIX):] if is_corpse else name]
    entity = factory(data["x"], data["y"])
    entity.energy = data["energy"]
    if "fighter" in data:
        for key, value in data["fighter"].items():
            setattr(entity.fighter, key, value)
    if "level" in data:
        for key, value in data["level"].items():
            setattr(entity.level, key, value)
    if "inventory" in data:
        entity.inventory.items = [entity_from_dict(item) for item in data["inventory"]]
        entity.equipment.slots = {"weapon": None, "armor": None}
        for index in data["equipped"]:
            item = entity.inventory.items[index]
            entity.equipment.slots[item.equippable.slot] = item
    if is_corpse:
        from ember import settings
        entity.char, entity.color, entity.name = "%", settings.CORPSE_RED, name
        entity.blocks_movement, entity.render_order = False, 0
    entity.ai = ai_from_dict(data["ai"], entity)
    return entity


def load_game(path=SAVE_PATH):
    data = json.loads(path.read_text())
    if data.get("version") != SAVE_VERSION:
        raise ValueError("This save file was made by a different version of the game.")
    world = game_world.GameWorld(data["seed"])
    world.depth = data["depth"]
    m = data["map"]
    game_map = GameMap(m["width"], m["height"])
    game_map.tiles = [[TILE_BY_NAME[name] for name in column] for column in m["tiles"]]
    game_map.explored = {tuple(cell) for cell in m["explored"]}
    entities = [entity_from_dict(e) for e in data["entities"]]
    engine = Engine(world, entities[data["player_index"]], generate=False)
    engine.game_map = game_map
    engine.entities = entities
    engine.turn = data["turn"]
    for text, color, count in data["messages"]:
        engine.message_log.add(text, tuple(color))
        engine.message_log.messages[-1].count = count
    engine.update_fov()
    return engine
