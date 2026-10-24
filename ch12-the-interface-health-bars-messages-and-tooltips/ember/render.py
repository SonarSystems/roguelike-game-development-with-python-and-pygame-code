# file: ember/render.py
"""Drawing single characters ("glyphs") into grid cells."""
import pygame

from ember import settings


class GlyphRenderer:
    """Renders characters with Pygame's built-in font and caches the results.

    Rendering text is slow compared with blitting a ready-made surface, so
    each (character, colour) pair is rendered once and reused every frame.
    """

    def __init__(self, font_size=settings.FONT_SIZE):
        self.font = pygame.font.Font(None, font_size)
        self.cache = {}

    def glyph(self, char, color):
        key = (char, color)
        if key not in self.cache:
            self.cache[key] = self.font.render(char, True, color)
        return self.cache[key]

    def draw(self, surface, char, x, y, color, background=None):
        """Draw `char` centred in grid cell (x, y)."""
        cell = pygame.Rect(x * settings.CELL_SIZE, y * settings.CELL_SIZE,
                           settings.CELL_SIZE, settings.CELL_SIZE)
        if background is not None:
            surface.fill(background, cell)
        image = self.glyph(char, color)
        surface.blit(image, image.get_rect(center=cell.center))

    def draw_text(self, surface, text, x, y, color):
        """Draw a whole string with its left edge at grid cell (x, y)."""
        image = self.font.render(text, True, color)
        top = y * settings.CELL_SIZE + (settings.CELL_SIZE - image.get_height()) // 2
        surface.blit(image, (x * settings.CELL_SIZE, top))
