def keep_largest_region(game_map):
    """Fill every floor pocket except the biggest one, so the cave is connected."""
    unvisited = set(game_map.floor_cells())
    best = set()
    while unvisited:
        region = game_map.reachable_from(*next(iter(unvisited)))
        unvisited -= region
        if len(region) > len(best):
            best = region
    for x, y in game_map.floor_cells():
        if (x, y) not in best:
            game_map.set_tile(x, y, tiles.WALL)
    return best
