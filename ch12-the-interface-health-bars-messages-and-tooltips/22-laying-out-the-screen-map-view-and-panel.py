def render_panel(surface, glyphs, engine):
    cell = settings.CELL_SIZE
    top = settings.PANEL_Y
    surface.fill(settings.PANEL_BG,
                 (0, top * cell, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - top * cell))
    fighter = engine.player.fighter
    render_bar(surface, glyphs, fighter.hp, fighter.max_hp, 1, top + 1, settings.BAR_WIDTH)
    glyphs.draw_text(surface, f"Turn: {engine.turn}", 1, top + 3, settings.WHITE)
    tooltip = names_at(engine, *engine.mouse_location)
    if tooltip:
        glyphs.draw_text(surface, tooltip, 1, top + 5, settings.TOOLTIP)
    log_width = settings.GRID_WIDTH - settings.LOG_X - 1
    render_message_log(surface, glyphs, engine.message_log, settings.LOG_X, top + 1,
                       log_width, settings.LOG_LINES)
