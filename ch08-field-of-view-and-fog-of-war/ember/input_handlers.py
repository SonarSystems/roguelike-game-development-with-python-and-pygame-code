# file: ember/input_handlers.py
"""Input handlers: turn Pygame events into Actions.

Each handler is one "mode" of the game. Later chapters add more modes
(inventory, targeting, game over) by adding more handler classes.
"""
import pygame

from ember.actions import EscapeAction, MovementAction, WaitAction

MOVE_KEYS = {
    # Arrow keys
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
    # Vi keys, the roguelike tradition (including diagonals)
    pygame.K_k: (0, -1), pygame.K_j: (0, 1),
    pygame.K_h: (-1, 0), pygame.K_l: (1, 0),
    pygame.K_y: (-1, -1), pygame.K_u: (1, -1),
    pygame.K_b: (-1, 1), pygame.K_n: (1, 1),
    # Numeric keypad
    pygame.K_KP8: (0, -1), pygame.K_KP2: (0, 1),
    pygame.K_KP4: (-1, 0), pygame.K_KP6: (1, 0),
    pygame.K_KP7: (-1, -1), pygame.K_KP9: (1, -1),
    pygame.K_KP1: (-1, 1), pygame.K_KP3: (1, 1),
}
WAIT_KEYS = {pygame.K_PERIOD, pygame.K_KP5}


class EventHandler:
    def __init__(self, engine):
        self.engine = engine

    def handle_event(self, event):
        """Return an Action for this event, or None."""
        return None


class MainGameEventHandler(EventHandler):
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        player = self.engine.player
        if event.key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[event.key]
            return MovementAction(player, dx, dy)
        if event.key in WAIT_KEYS:
            return WaitAction(player)
        if event.key == pygame.K_ESCAPE:
            return EscapeAction(player)
        return None
