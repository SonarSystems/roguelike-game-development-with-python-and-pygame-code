def names_at(engine, x, y):
    if not engine.game_map.in_bounds(x, y) or (x, y) not in engine.game_map.visible:
        return ""
    names = [e.name for e in engine.entities if e.x == x and e.y == y]
    return ", ".join(name[0].upper() + name[1:] for name in names)
