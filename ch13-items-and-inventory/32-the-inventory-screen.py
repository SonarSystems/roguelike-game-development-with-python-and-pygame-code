import pygame

if event.key == pygame.K_i:
    self.engine.event_handler = InventoryActivateHandler(self.engine)
elif event.key == pygame.K_d:
    self.engine.event_handler = InventoryDropHandler(self.engine)
