def draw(self, surface, glyphs):
    for x in range(self.width):
        for y in range(self.height):
            tile = self.tiles[x][y]
            glyphs.draw(surface, tile.glyph, x, y, tile.color, tile.background)
