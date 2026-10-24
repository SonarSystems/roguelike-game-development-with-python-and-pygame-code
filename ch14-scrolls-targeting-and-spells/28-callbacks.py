class AreaTargetHandler(SingleTargetHandler):
    """Like SingleTargetHandler, but outlines every cell the effect will reach."""

    def __init__(self, engine, radius, callback):
        super().__init__(engine, callback)
        self.radius = radius

    def highlighted_cells(self):
        cx, cy = self.cursor
        r = self.radius
        return [(x, y) for x in range(cx - r, cx + r + 1) for y in range(cy - r, cy + r + 1)]
