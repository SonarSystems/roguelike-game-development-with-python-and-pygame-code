import pygame
import random
import sys
import time

async def main_async():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None

    error = None
    while True:
        choice = await run_main_menu(screen, glyphs, clock, error)
        error = None
        if choice == NEW_GAME:
            engine = new_game(seed_arg if seed_arg is not None else random.randrange(1_000_000))
        elif choice == CONTINUE:
            try:
                engine = load_game()
            except (OSError, ValueError, KeyError) as exc:
                error = f"Couldn't load the saved game: {exc}"
                continue
        else:
            break
        try:
            await play(engine, screen, glyphs, clock)
        except NewGame:
            continue                      # back to the title screen
        except SystemExit:
            # Quitting mid-run saves it; a finished run has nothing to save.
            if not isinstance(engine.event_handler, GameOverEventHandler):
                save_game(engine)
            break
    pygame.quit()
