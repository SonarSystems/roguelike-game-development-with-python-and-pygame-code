import pygame

if event.type == pygame.MOUSEMOTION:
    self.mouse_location = (event.pos[0] // settings.CELL_SIZE,
                           event.pos[1] // settings.CELL_SIZE)
