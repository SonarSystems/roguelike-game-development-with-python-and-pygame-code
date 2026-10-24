# file: ember/ui.py
"""Drawing the interface panel: health bar, message log and mouse-over names."""
import pygame

from ember import settings


def render_bar(surface, glyphs, current, maximum, x, y, width):
    cell = settings.CELL_SIZE
    full = pygame.Rect(x * cell, y * cell, width * cell, cell)
    surface.fill(settings.BAR_EMPTY, full)
    filled_width = int(full.width * current / maximum) if maximum else 0
    if filled_width > 0:
        surface.fill(settings.BAR_FILLED, (full.x, full.y, filled_width, cell))
    glyphs.draw_text(surface, f" HP: {current}/{maximum}", x, y, settings.WHITE)


def render_message_log(surface, glyphs, message_log, x, y, width, height):
    # Roughly two characters fit in each cell with Pygame's default font.
    lines = message_log.recent_lines(width * 2, height)
    for i, (text, color) in enumerate(lines):
        glyphs.draw_text(surface, text, x, y + i, color)


def names_at(engine, x, y):
    if not engine.game_map.in_bounds(x, y) or (x, y) not in engine.game_map.visible:
        return ""
    names = [e.name for e in engine.entities if e.x == x and e.y == y]
    return ", ".join(name[0].upper() + name[1:] for name in names)


def render_panel(surface, glyphs, engine):
    cell = settings.CELL_SIZE
    top = settings.PANEL_Y
    surface.fill(settings.PANEL_BG,
                 (0, top * cell, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - top * cell))
    fighter = engine.player.fighter
    render_bar(surface, glyphs, fighter.hp, fighter.max_hp, 1, top + 1, settings.BAR_WIDTH)
    glyphs.draw_text(surface, f"Depth: {engine.game_world.depth}    Turn: {engine.turn}",
                     1, top + 3, settings.WHITE)
    tooltip = names_at(engine, *engine.mouse_location)
    if tooltip:
        glyphs.draw_text(surface, tooltip, 1, top + 5, settings.TOOLTIP)
    log_width = settings.GRID_WIDTH - settings.LOG_X - 1
    render_message_log(surface, glyphs, engine.message_log, settings.LOG_X, top + 1,
                       log_width, settings.LOG_LINES)
