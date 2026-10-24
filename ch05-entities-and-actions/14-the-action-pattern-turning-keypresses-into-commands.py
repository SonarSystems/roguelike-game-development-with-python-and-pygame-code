class MovementAction(ActionWithDirection):
    def perform(self, engine):
        dest_x, dest_y = self.destination
        if not engine.game_map.is_walkable(dest_x, dest_y):
            return  # bumped into a wall: nothing happens
        if engine.blocking_entity_at(dest_x, dest_y):
            return  # something is standing there
        self.entity.move(self.dx, self.dy)
