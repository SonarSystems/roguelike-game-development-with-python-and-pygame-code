# file: ember/engine.py
"""The Engine owns the game state and connects input, actions and drawing."""
from ember import settings
from ember.fov import compute_fov
from ember.input_handlers import MainGameEventHandler

FOV_RADIUS = 8
ACTION_COST = 100   # energy an entity spends to take one action


class Engine:
    def __init__(self, game_map, player, entities):
        self.game_map = game_map
        self.player = player
        self.entities = entities          # includes the player
        self.turn = 0
        self.message = ""
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
        if action is None:
            return
        action.perform(self)
        self.turn += 1
        self.run_monster_turns()
        self.update_fov()

    def run_monster_turns(self):
        """The energy system: every monster gains its speed in energy and
        acts once for every ACTION_COST it has banked. Fast monsters act
        more than once per player turn; slow ones skip turns."""
        for entity in list(self.entities):
            if entity.ai is None:
                continue
            entity.energy += entity.speed
            while entity.energy >= ACTION_COST:
                entity.energy -= ACTION_COST
                entity.ai.decide(self).perform(self)

    def render(self, surface, glyphs):
        surface.fill(settings.BLACK)
        self.game_map.draw(surface, glyphs)
        for entity in self.entities:
            if (entity.x, entity.y) in self.game_map.visible:
                tile = self.game_map.tiles[entity.x][entity.y]
                glyphs.draw(surface, entity.char, entity.x, entity.y, entity.color, tile.background)
        glyphs.draw_text(surface, f"Turn: {self.turn}   {self.message}", 1,
                         settings.GRID_HEIGHT - 2, settings.WHITE)
