def draw(self, surface, glyphs, camera, offset=(0, 0)):
    """Draw the part of the map inside the camera's view.

    Visible cells in full colour, remembered cells dimmed, the rest black.
    `offset` is an extra pixel shift, used for screen shake.
    """
    cell = camera.cell_size
    left, top = int(camera.x), int(camera.y)
    for x in range(left, left + camera.width + 1):
        for y in range(top, top + camera.height + 1):
            if (x, y) not in self.explored:
                continue
            px, py = camera.to_pixels(x, y)
            px, py = px + offset[0], py + offset[1]
            tile = self.tiles[x][y]
            if (x, y) in self.visible:
                glyphs.draw_px(surface, tile.glyph, px, py, tile.color, tile.background)
            else:
                glyphs.draw_px(surface, tile.glyph, px, py, darken(tile.color),
                               darken(tile.background))
