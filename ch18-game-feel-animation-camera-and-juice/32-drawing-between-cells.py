import pygame

def draw_px(self, surface, char, px, py, color, background=None):
    """Draw `char` in the cell whose top-left corner is at pixel (px, py).

    Used for smooth movement and scrolling, where things sit between cells.
    """
    cell = pygame.Rect(round(px), round(py), settings.CELL_SIZE, settings.CELL_SIZE)
    if background is not None:
        surface.fill(background, cell)
    image = self.glyph(char, color)
    surface.blit(image, image.get_rect(center=cell.center))
