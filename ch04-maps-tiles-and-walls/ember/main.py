# file: ember/main.py
"""Entry point: open the window and run the game loop."""
import pygame

from ember import settings
from ember.game_map import build_test_map
from ember.render import GlyphRenderer

MOVE_KEYS = {
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
    pygame.K_k: (0, -1), pygame.K_j: (0, 1),
    pygame.K_h: (-1, 0), pygame.K_l: (1, 0),
}


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()

    game_map = build_test_map(settings.GRID_WIDTH, settings.GRID_HEIGHT - 2)
    player_x, player_y = 10, 10
    turns = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in MOVE_KEYS:
                    dx, dy = MOVE_KEYS[event.key]
                    new_x, new_y = player_x + dx, player_y + dy
                    if game_map.is_walkable(new_x, new_y):
                        player_x, player_y = new_x, new_y
                        turns += 1

        screen.fill(settings.BLACK)
        game_map.draw(screen, glyphs)
        glyphs.draw(screen, "@", player_x, player_y, settings.EMBER)
        glyphs.draw_text(screen, f"Turns: {turns}", 1, settings.GRID_HEIGHT - 1, settings.WHITE)
        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
