def draw_distance_overlay(self, surface, glyphs):
    """Debug view: each visible floor cell shows its distance to the
    player (last digit only, so it fits in one cell)."""
    field = dijkstra_map(self.game_map, [(self.player.x, self.player.y)])
    for (x, y), distance in field.items():
        if (x, y) in self.game_map.visible and (x, y) != (self.player.x, self.player.y):
            background = self.game_map.tiles[x][y].background
            glyphs.draw(surface, str(distance % 10), x, y, (120, 200, 255), background)
