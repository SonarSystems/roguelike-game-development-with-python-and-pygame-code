class TakeStairsAction(Action):
    def perform(self, engine):
        x, y = self.entity.x, self.entity.y
        if engine.game_map.tiles[x][y] is not tiles.DOWN_STAIRS:
            raise Impossible("There are no stairs here.")
        engine.game_world.generate_floor(engine)
        engine.log(f"You descend to depth {engine.game_world.depth}.", settings.DESCEND)
