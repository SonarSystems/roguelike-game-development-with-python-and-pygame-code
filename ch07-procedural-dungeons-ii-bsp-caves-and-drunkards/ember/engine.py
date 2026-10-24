# file: ember/engine.py
"""The Engine owns the game state and connects input, actions and drawing."""
from ember import settings
from ember.input_handlers import MainGameEventHandler


class Engine:
    def __init__(self, game_map, player, entities):
        self.game_map = game_map
        self.player = player
        self.entities = entities          # includes the player
        self.turn = 0
        self.event_handler = MainGameEventHandler(self)

    def blocking_entity_at(self, x, y):
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

    def handle_event(self, event):
        action = self.event_handler.handle_event(event)
        if action is not None:
            action.perform(self)
            self.turn += 1

    def render(self, surface, glyphs):
        surface.fill(settings.BLACK)
        self.game_map.draw(surface, glyphs)
        for entity in self.entities:
            tile = self.game_map.tiles[entity.x][entity.y]
            glyphs.draw(surface, entity.char, entity.x, entity.y, entity.color, tile.background)
        glyphs.draw_text(surface, f"Turn: {self.turn}", 1, settings.GRID_HEIGHT - 1, settings.WHITE)
