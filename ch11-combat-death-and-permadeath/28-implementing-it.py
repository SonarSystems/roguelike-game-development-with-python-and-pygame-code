import pygame

class GameOverEventHandler(EventHandler):
    """The player is dead. No actions are possible: only a new run or quitting."""

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_ESCAPE:
            raise SystemExit()
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            raise NewGame()
        return None

    def on_render(self, surface, glyphs):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))
        lines = ["YOU HAVE DIED", f"You survived {self.engine.turn} turns.",
                 "Enter: start a new run    Esc: quit"]
        for i, text in enumerate(lines):
            image = glyphs.font.render(text, True, (240, 200, 160))
            rect = image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 30 + i * 32))
            surface.blit(image, rect)
