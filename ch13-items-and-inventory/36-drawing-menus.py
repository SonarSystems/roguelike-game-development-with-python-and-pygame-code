import pygame

def draw_box(surface, glyphs, title, lines, x, y, width):
    """A framed menu box drawn in grid cells, used by every pop-up screen."""
    cell = settings.CELL_SIZE
    height = len(lines) + 3
    rect = pygame.Rect(x * cell, y * cell, width * cell, height * cell)
    surface.fill(settings.PANEL_BG, rect)
    pygame.draw.rect(surface, settings.MENU_TITLE, rect, width=2)
    glyphs.draw_text(surface, title, x + 1, y + 1, settings.MENU_TITLE)
    for i, line in enumerate(lines):
        glyphs.draw_text(surface, line, x + 1, y + 2 + i, settings.MENU_TEXT)
