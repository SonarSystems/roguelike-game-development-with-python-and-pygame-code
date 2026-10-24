# file: ember/main_menu.py
"""The title screen: new game, continue, or quit."""
import pygame

from ember import settings
from ember.savegame import SAVE_PATH

NEW_GAME, CONTINUE, QUIT = "new", "continue", "quit"


def run_main_menu(screen, glyphs, clock, error=None):
    """Show the menu until the player chooses. Returns NEW_GAME, CONTINUE or QUIT."""
    has_save = SAVE_PATH.exists()
    title_font = pygame.font.Font(None, 96)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return NEW_GAME
                if event.key == pygame.K_c and has_save:
                    return CONTINUE
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return QUIT

        screen.fill(settings.BLACK)
        centre_x = screen.get_width() // 2
        title = title_font.render("EMBER DEPTHS", True, settings.EMBER)
        screen.blit(title, title.get_rect(center=(centre_x, 240)))
        subtitle = glyphs.font.render("Descend ten floors. Claim the Ember Crown. Die only once.",
                                      True, (200, 180, 160))
        screen.blit(subtitle, subtitle.get_rect(center=(centre_x, 310)))
        options = ["[N] New game", "[C] Continue" if has_save else "[C] Continue (no saved game)",
                   "[Q] Quit"]
        for i, text in enumerate(options):
            color = settings.WHITE if (i != 1 or has_save) else (110, 110, 110)
            image = glyphs.font.render(text, True, color)
            screen.blit(image, image.get_rect(center=(centre_x, 400 + i * 40)))
        if error:
            image = glyphs.font.render(error, True, settings.DEATH_RED)
            screen.blit(image, image.get_rect(center=(centre_x, 560)))
        pygame.display.flip()
        clock.tick(settings.FPS)
