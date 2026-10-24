def recent_lines(self, width_chars, height):
    """The newest `height` wrapped lines, oldest first, as (text, colour)."""
    lines = []
    for message in reversed(self.messages):
        wrapped = textwrap.wrap(message.full_text, width_chars) or [""]
        for line in reversed(wrapped):
            lines.append((line, message.color))
            if len(lines) == height:
                return lines[::-1]
    return lines[::-1]
