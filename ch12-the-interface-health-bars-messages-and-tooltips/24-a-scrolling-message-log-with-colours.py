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
