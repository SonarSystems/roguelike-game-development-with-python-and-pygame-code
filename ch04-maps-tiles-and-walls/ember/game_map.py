# file: ember/game_map.py
"""The dungeon map: a 2D grid of tiles."""
from ember import tiles


class GameMap:
    def __init__(self, width, height, fill=tiles.WALL):
        self.width = width
        self.height = height
        # tiles[x][y] — a list of columns, so tiles[x][y] reads like (x, y).
        self.tiles = [[fill for _ in range(height)] for _ in range(width)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x, y):
        return self.in_bounds(x, y) and self.tiles[x][y].walkable

    def set_tile(self, x, y, tile):
        if self.in_bounds(x, y):
            self.tiles[x][y] = tile

    def draw(self, surface, glyphs):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                glyphs.draw(surface, tile.glyph, x, y, tile.color, tile.background)


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
