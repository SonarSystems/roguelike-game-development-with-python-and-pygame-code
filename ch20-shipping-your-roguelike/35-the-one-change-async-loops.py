import pygame

async def play(engine, screen, glyphs, clock):
    """Run one game until the player quits or starts a new run."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()
            engine.handle_event(event)
        dt = clock.tick(settings.FPS) / 1000.0   # seconds since the last frame
        engine.render(screen, glyphs, dt)
        pygame.display.flip()
        await asyncio.sleep(0)
