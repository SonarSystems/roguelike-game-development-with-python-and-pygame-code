def __init__(self, game_world, player):
    self.game_world = game_world
    ...
    self.game_map = None              # set by game_world.generate_floor()
    self.entities = []                # includes the player
    ...
    game_world.generate_floor(self)
