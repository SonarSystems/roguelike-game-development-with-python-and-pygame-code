# file: ember/engine.py
"""The Engine owns the game state and connects input, actions and drawing."""
import pygame

from ember import settings, ui
from ember.exceptions import Impossible
from ember.fov import compute_fov
from ember.input_handlers import (GameOverEventHandler, LevelUpEventHandler,
                                  MainGameEventHandler, VictoryEventHandler)
from ember.message_log import MessageLog
from ember.pathfinding import dijkstra_map

FOV_RADIUS = 8
ACTION_COST = 100   # energy an entity spends to take one action


class Engine:
    def __init__(self, game_world, player):
        self.game_world = game_world
        self.player = player
        self.game_map = None              # set by game_world.generate_floor()
        self.entities = []                # includes the player
        self.turn = 0
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)      # grid cell under the mouse pointer
        self.show_distances = False       # F1 toggles the Dijkstra-map debug overlay
        self.event_handler = MainGameEventHandler(self)
        game_world.generate_floor(self)

    def log(self, text, color=settings.WHITE):
        self.message_log.add(text, color)

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

    def on_player_death(self):
        self.event_handler = GameOverEventHandler(self)

    def on_victory(self):
        self.event_handler = VictoryEventHandler(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_location = (event.pos[0] // settings.CELL_SIZE,
                                   event.pos[1] // settings.CELL_SIZE)
        action = self.event_handler.handle_event(event)
        if action is None:
            return
        try:
            action.perform(self)
        except Impossible as reason:
            self.log(str(reason), settings.IMPOSSIBLE)
            return          # an impossible action doesn't use up a turn
        self.turn += 1
        if self.player.is_alive:
            self.run_monster_turns()
        self.update_fov()
        if self.player.is_alive and self.player.level.requires_level_up:
            self.event_handler = LevelUpEventHandler(self)

    def run_monster_turns(self):
        """The energy system: every monster gains its speed in energy and
        acts once for every ACTION_COST it has banked. Fast monsters act
        more than once per player turn; slow ones skip turns."""
        for entity in list(self.entities):
            if entity.ai is None:
                continue
            entity.energy += entity.speed
            while entity.energy >= ACTION_COST and entity.ai is not None:
                entity.energy -= ACTION_COST
                entity.ai.decide(self).perform(self)
                if not self.player.is_alive:
                    return

    def render(self, surface, glyphs):
        surface.fill(settings.BLACK)
        self.game_map.draw(surface, glyphs)
        if self.show_distances:
            self.draw_distance_overlay(surface, glyphs)
        for entity in sorted(self.entities, key=lambda e: e.render_order):
            if (entity.x, entity.y) in self.game_map.visible:
                tile = self.game_map.tiles[entity.x][entity.y]
                glyphs.draw(surface, entity.char, entity.x, entity.y, entity.color, tile.background)
        ui.render_panel(surface, glyphs, self)
        self.event_handler.on_render(surface, glyphs)

    def draw_distance_overlay(self, surface, glyphs):
        """Debug view: each visible floor cell shows its distance to the
        player (last digit only, so it fits in one cell)."""
        field = dijkstra_map(self.game_map, [(self.player.x, self.player.y)])
        for (x, y), distance in field.items():
            if (x, y) in self.game_map.visible and (x, y) != (self.player.x, self.player.y):
                background = self.game_map.tiles[x][y].background
                glyphs.draw(surface, str(distance % 10), x, y, (120, 200, 255), background)
