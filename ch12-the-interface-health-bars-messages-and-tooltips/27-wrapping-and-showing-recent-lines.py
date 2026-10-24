def render_message_log(surface, glyphs, message_log, x, y, width, height):
    # Roughly two characters fit in each cell with Pygame's default font.
    lines = message_log.recent_lines(width * 2, height)
    for i, (text, color) in enumerate(lines):
        glyphs.draw_text(surface, text, x, y + i, color)
