def is_transparent(self, x, y):
    return self.in_bounds(x, y) and self.tiles[x][y].transparent
