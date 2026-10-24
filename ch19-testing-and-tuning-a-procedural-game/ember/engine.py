# file: ember/engine.py
"""The Engine owns the game state and connects input, actions and drawing."""
import random

import pygame

from ember import settings, ui
from ember.camera import Camera
from ember.effects import Effects
from ember.exceptions import Impossible
from ember.fov import compute_fov
from ember.input_handlers import (GameOverEventHandler, LevelUpEventHandler,
                                  MainGameEventHandler, VictoryEventHandler)
from ember.message_log import MessageLog
from ember.pathfinding import dijkstra_map

FOV_RADIUS = 8
ACTION_COST = 100   # energy an entity spends to take one action


class Engine:
    def __init__(self, game_world, player, generate=True):
        self.game_world = game_world
        self.player = player
        # All gameplay randomness after map generation comes from here,
        # so the same seed and the same keypresses replay the same run.
        self.rng = random.Random(game_world.seed)
        self.game_map = None              # set by game_world.generate_floor()
        self.entities = []                # includes the player
        self.turn = 0
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)      # grid cell under the mouse pointer
        self.show_distances = False       # F1 toggles the Dijkstra-map debug overlay
        self.event_handler = MainGameEventHandler(self)
        self.camera = Camera()
        self.effects = Effects()
        if generate:                       # loading a save skips this
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
        from ember.savegame import delete_save
        delete_save()                      # permadeath: there is no going back
        self.event_handler = GameOverEventHandler(self)

    def on_victory(self):
        from ember.savegame import delete_save
        delete_save()
        self.event_handler = VictoryEventHandler(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_location = self.camera.screen_to_world(*event.pos)
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

    def render(self, surface, glyphs, dt=0.0):
        """Draw one frame. `dt` is the time since the last frame, in seconds."""
        self.effects.update(dt, self.entities)
        # The camera follows where the player is *drawn*, so it glides too.
        self.camera.follow(*self.effects.visual_position(self.player),
                           self.game_map.width, self.game_map.height)
        offset = self.effects.shake_offset()
        cell = settings.CELL_SIZE

        surface.fill(settings.BLACK)
        surface.set_clip((0, 0, settings.VIEW_WIDTH * cell, settings.VIEW_HEIGHT * cell))
        self.game_map.draw(surface, glyphs, self.camera, offset)
        if self.show_distances:
            self.draw_distance_overlay(surface, glyphs)
        for entity in sorted(self.entities, key=lambda e: e.render_order):
            if (entity.x, entity.y) not in self.game_map.visible:
                continue
            vx, vy = self.effects.visual_position(entity)
            px, py = self.camera.to_pixels(vx, vy)
            color = (255, 255, 255) if self.effects.is_flashing(entity) else entity.color
            glyphs.draw_px(surface, entity.char, px + offset[0], py + offset[1], color)
        self.effects.draw_floaters(surface, glyphs.font, self.camera, offset)
        surface.set_clip(None)
        ui.render_panel(surface, glyphs, self)
        self.event_handler.on_render(surface, glyphs)

    def draw_distance_overlay(self, surface, glyphs):
        """Debug view: each visible floor cell shows its distance to the
        player (last digit only, so it fits in one cell)."""
        field = dijkstra_map(self.game_map, [(self.player.x, self.player.y)])
        for (x, y), distance in field.items():
            if (x, y) in self.game_map.visible and (x, y) != (self.player.x, self.player.y):
                px, py = self.camera.to_pixels(x, y)
                background = self.game_map.tiles[x][y].background
                glyphs.draw_px(surface, str(distance % 10), px, py, (120, 200, 255), background)
