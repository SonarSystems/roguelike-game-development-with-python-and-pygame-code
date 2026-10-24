# file: ember/main.py
"""Entry point: build the game, then run the loop."""
import pygame

from ember import settings
from ember.engine import Engine
from ember.entity import Entity
from ember.game_map import build_test_map
from ember.render import GlyphRenderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()

    game_map = build_test_map(settings.GRID_WIDTH, settings.GRID_HEIGHT - 2)
    player = Entity(10, 10, "@", settings.EMBER, "Player", blocks_movement=True)
    statue = Entity(30, 20, "&", (200, 200, 255), "Statue", blocks_movement=True)
    engine = Engine(game_map, player, [statue, player])

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                engine.handle_event(event)
            engine.render(screen, glyphs)
            pygame.display.flip()
            clock.tick(settings.FPS)
    except SystemExit:
        pygame.quit()


if __name__ == "__main__":
    main()
