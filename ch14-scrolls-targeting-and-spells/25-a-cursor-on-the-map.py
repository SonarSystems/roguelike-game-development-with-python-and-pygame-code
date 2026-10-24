import pygame

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
