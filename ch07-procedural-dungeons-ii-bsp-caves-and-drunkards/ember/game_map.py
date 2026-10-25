# file: ember/game_map.py
"""The dungeon map: a 2D grid of tiles."""
from collections import deque

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

    def reachable_from(self, x, y):
        """Flood fill: every walkable cell you can walk to from (x, y)."""
        seen = {(x, y)}
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in seen and self.is_walkable(nx, ny):
                    seen.add((nx, ny))
                    queue.append((nx, ny))
        return seen

    def floor_cells(self):
        return [(x, y) for x in range(self.width) for y in range(self.height)
                if self.tiles[x][y].walkable]

    def draw(self, surface, glyphs):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                glyphs.draw(surface, tile.glyph, x, y, tile.color, tile.background)

