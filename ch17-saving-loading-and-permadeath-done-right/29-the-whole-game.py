import json

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
