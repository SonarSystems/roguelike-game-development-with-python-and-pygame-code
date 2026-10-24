import json

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
