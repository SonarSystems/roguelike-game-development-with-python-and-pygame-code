def build_test_map(width, height):
    """A hand-made map for testing: one big room with a pillar and a wall."""
    game_map = GameMap(width, height)
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            game_map.set_tile(x, y, tiles.FLOOR)
    for x in range(20, 26):              # a 6x4 pillar
        for y in range(10, 14):
            game_map.set_tile(x, y, tiles.WALL)
    for y in range(1, height - 8):       # a dividing wall with a gap at the bottom
        game_map.set_tile(40, y, tiles.WALL)
    return game_map
