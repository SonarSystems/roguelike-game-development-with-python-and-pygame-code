# file: ember/engine.py
"""The Engine owns the game state and connects input, actions and drawing."""
from ember import settings
from ember.fov import compute_fov
from ember.input_handlers import MainGameEventHandler

FOV_RADIUS = 8


class Engine:
    def __init__(self, game_map, player, entities):
        self.game_map = game_map
        self.player = player
        self.entities = entities          # includes the player
        self.turn = 0
        self.event_handler = MainGameEventHandler(self)
        self.update_fov()

    def blocking_entity_at(self, x, y):
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

    def update_fov(self):
        player = self.player
        self.game_map.visible = compute_fov(self.game_map.is_transparent,
                                            player.x, player.y, FOV_RADIUS)
        self.game_map.explored |= self.game_map.visible

    def handle_event(self, event):
        action = self.event_handler.handle_event(event)
        if action is not None:
            action.perform(self)
            self.turn += 1
            self.update_fov()

    def render(self, surface, glyphs):
        surface.fill(settings.BLACK)
        self.game_map.draw(surface, glyphs)
        for entity in self.entities:
            if (entity.x, entity.y) in self.game_map.visible:
                tile = self.game_map.tiles[entity.x][entity.y]
                glyphs.draw(surface, entity.char, entity.x, entity.y, entity.color, tile.background)
        glyphs.draw_text(surface, f"Turn: {self.turn}", 1, settings.GRID_HEIGHT - 1, settings.WHITE)
