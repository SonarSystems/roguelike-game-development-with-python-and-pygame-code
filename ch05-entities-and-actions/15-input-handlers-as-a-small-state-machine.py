import pygame

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
