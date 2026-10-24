def draw(self, surface, glyphs):
    """Visible cells in full colour, remembered cells dimmed, the rest black."""
    for x, y in self.explored:
        tile = self.tiles[x][y]
        if (x, y) in self.visible:
            glyphs.draw(surface, tile.glyph, x, y, tile.color, tile.background)
        else:
            glyphs.draw(surface, tile.glyph, x, y, darken(tile.color), darken(tile.background))
