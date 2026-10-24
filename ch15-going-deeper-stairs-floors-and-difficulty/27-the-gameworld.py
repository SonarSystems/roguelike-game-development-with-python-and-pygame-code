class GameWorld:
    def __init__(self, seed):
        self.seed = seed
        self.depth = 0

    def generate_floor(self, engine):
        """Build the next floor down, and move the player onto it."""
        self.depth += 1
        floor_seed = self.seed * 1000 + self.depth   # one reproducible seed per floor
        game_map, rooms = generate_level(floor_seed, settings.MAP_WIDTH, settings.MAP_HEIGHT)
        start = rooms[0].center

        # Put the stairs (or, on the last floor, the crown) as far from the
        # start as possible, so every floor has to be crossed.
        distances = game_map.reachable_from(*start)
        far_cell = max(distances, key=lambda c: abs(c[0] - start[0]) + abs(c[1] - start[1]))
        extras = []
        if self.depth < FINAL_DEPTH:
            game_map.set_tile(*far_cell, tiles.DOWN_STAIRS)
        else:
            extras.append(ember_crown(*far_cell))

        player = engine.player
        player.x, player.y = start
        others = populate(self.seed, self.depth, game_map, start, avoid={far_cell})
        items = [e for e in others if e.is_item]
        monsters = [e for e in others if not e.is_item]
        engine.game_map = game_map
        engine.entities = extras + items + monsters + [player]
        engine.update_fov()
