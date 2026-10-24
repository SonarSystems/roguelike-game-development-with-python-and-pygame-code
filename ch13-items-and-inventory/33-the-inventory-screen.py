import pygame

class InventoryEventHandler(EventHandler):
    """Shows the inventory; pressing a letter picks an item. Esc goes back."""

    TITLE = "Inventory"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_ESCAPE:
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return None
        index = event.key - pygame.K_a
        items = self.engine.player.inventory.items
        if 0 <= index < len(items):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return self.on_item_selected(items[index])
        return None

    def on_item_selected(self, item):
        raise NotImplementedError()

    def on_render(self, surface, glyphs):
        items = self.engine.player.inventory.items
        lines = [f"({chr(ord('a') + i)}) {item.name}" for i, item in enumerate(items)]
        if not lines:
            lines = ["(empty)"]
        draw_box(surface, glyphs, f"{self.TITLE}  (Esc to close)", lines, 2, 2, 28)
