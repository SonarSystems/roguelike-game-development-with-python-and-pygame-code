# file: ember/message_log.py
"""The message log: everything that happens, as coloured lines of text."""
import textwrap


class Message:
    def __init__(self, text, color):
        self.plain_text = text
        self.color = color
        self.count = 1

    @property
    def full_text(self):
        """Repeated messages are stacked: 'The rat bites you. (x3)'."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self):
        self.messages = []

    def add(self, text, color, stack=True):
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, color))

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
