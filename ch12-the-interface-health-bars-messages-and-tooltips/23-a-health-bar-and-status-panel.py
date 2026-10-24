import pygame

def render_bar(surface, glyphs, current, maximum, x, y, width):
    cell = settings.CELL_SIZE
    full = pygame.Rect(x * cell, y * cell, width * cell, cell)
    surface.fill(settings.BAR_EMPTY, full)
    filled_width = int(full.width * current / maximum) if maximum else 0
    if filled_width > 0:
        surface.fill(settings.BAR_FILLED, (full.x, full.y, filled_width, cell))
    glyphs.draw_text(surface, f" HP: {current}/{maximum}", x, y, settings.WHITE)
