# file: ember/input_handlers.py
"""Input handlers: turn Pygame events into Actions.

Each handler is one "mode" of the game. The engine always sends events
to whichever handler is current, and a handler can switch the engine
to a different mode by replacing engine.event_handler.
"""
import pygame

from ember import settings
from ember.actions import (BumpAction, DropAction, EscapeAction, PickupAction,
                           TakeStairsAction, WaitAction)

MOVE_KEYS = {
    # Arrow keys
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
    # Vi keys, the roguelike tradition (including diagonals)
    pygame.K_k: (0, -1), pygame.K_j: (0, 1),
    pygame.K_h: (-1, 0), pygame.K_l: (1, 0),
    pygame.K_y: (-1, -1), pygame.K_u: (1, -1),
    pygame.K_b: (-1, 1), pygame.K_n: (1, 1),
    # Numeric keypad
    pygame.K_KP8: (0, -1), pygame.K_KP2: (0, 1),
    pygame.K_KP4: (-1, 0), pygame.K_KP6: (1, 0),
    pygame.K_KP7: (-1, -1), pygame.K_KP9: (1, -1),
    pygame.K_KP1: (-1, 1), pygame.K_KP3: (1, 1),
}
WAIT_KEYS = {pygame.K_PERIOD, pygame.K_KP5}


class NewGame(Exception):
    """Raised to throw away the current run and start a fresh one."""


class EventHandler:
    def __init__(self, engine):
        self.engine = engine

    def handle_event(self, event):
        """Return an Action for this event, or None."""
        return None

    def on_render(self, surface, glyphs):
        """Draw anything this mode adds on top of the map."""


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


class MainGameEventHandler(EventHandler):
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        player = self.engine.player
        if event.key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[event.key]
            return BumpAction(player, dx, dy)
        if event.unicode == ">":                 # Shift + . on most keyboards
            return TakeStairsAction(player)
        if event.key in WAIT_KEYS:
            return WaitAction(player)
        if event.key == pygame.K_g:
            return PickupAction(player)
        if event.key == pygame.K_i:
            self.engine.event_handler = InventoryActivateHandler(self.engine)
        elif event.key == pygame.K_d:
            self.engine.event_handler = InventoryDropHandler(self.engine)
        elif event.key == pygame.K_ESCAPE:
            return EscapeAction(player)
        elif event.key == pygame.K_F1:
            self.engine.show_distances = not self.engine.show_distances
        return None


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


class InventoryActivateHandler(InventoryEventHandler):
    TITLE = "Use which item?"

    def on_item_selected(self, item):
        # The item decides: use it now, or switch to a targeting mode first.
        return item.consumable.get_action(self.engine.player, self.engine)


class InventoryDropHandler(InventoryEventHandler):
    TITLE = "Drop which item?"

    def on_item_selected(self, item):
        return DropAction(self.engine.player, item)


class SelectCellHandler(EventHandler):
    """Move a cursor around the map with the movement keys or the mouse.

    Enter, or a left click, confirms the cell; Esc cancels.
    """

    def __init__(self, engine):
        super().__init__(engine)
        player = engine.player
        self.cursor = (player.x, player.y)
        engine.mouse_location = self.cursor

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.cursor = self.engine.mouse_location
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.confirm(self.engine.mouse_location)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.event_handler = MainGameEventHandler(self.engine)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.confirm(self.cursor)
            elif event.key in MOVE_KEYS:
                dx, dy = MOVE_KEYS[event.key]
                x = min(max(0, self.cursor[0] + dx), self.engine.game_map.width - 1)
                y = min(max(0, self.cursor[1] + dy), self.engine.game_map.height - 1)
                self.cursor = (x, y)
                self.engine.mouse_location = self.cursor
        return None

    def confirm(self, cell):
        self.engine.event_handler = MainGameEventHandler(self.engine)
        return self.on_selected(cell)

    def on_selected(self, cell):
        raise NotImplementedError()

    def highlighted_cells(self):
        return [self.cursor]

    def on_render(self, surface, glyphs):
        cell_size = settings.CELL_SIZE
        for x, y in self.highlighted_cells():
            if self.engine.game_map.in_bounds(x, y):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, settings.TARGET_HIGHLIGHT, rect, width=1)


class SingleTargetHandler(SelectCellHandler):
    def __init__(self, engine, callback):
        super().__init__(engine)
        self.callback = callback    # turns the chosen cell into an Action

    def on_selected(self, cell):
        return self.callback(cell)


class AreaTargetHandler(SingleTargetHandler):
    """Like SingleTargetHandler, but outlines every cell the effect will reach."""

    def __init__(self, engine, radius, callback):
        super().__init__(engine, callback)
        self.radius = radius

    def highlighted_cells(self):
        cx, cy = self.cursor
        r = self.radius
        return [(x, y) for x in range(cx - r, cx + r + 1) for y in range(cy - r, cy + r + 1)]


class GameOverEventHandler(EventHandler):
    """The run is over. No actions are possible: only a new run or quitting."""

    HEADLINE = "YOU HAVE DIED"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_ESCAPE:
            raise SystemExit()
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            raise NewGame()
        return None

    def on_render(self, surface, glyphs):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))
        lines = [self.HEADLINE, f"Depth {self.engine.game_world.depth}, {self.engine.turn} turns.",
                 "Enter: start a new run    Esc: quit"]
        for i, text in enumerate(lines):
            image = glyphs.font.render(text, True, (240, 200, 160))
            rect = image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 30 + i * 32))
            surface.blit(image, rect)


class VictoryEventHandler(GameOverEventHandler):
    HEADLINE = "YOU ESCAPED WITH THE EMBER CROWN!"
