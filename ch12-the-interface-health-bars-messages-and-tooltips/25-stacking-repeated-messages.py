def add(self, text, color, stack=True):
    if stack and self.messages and self.messages[-1].plain_text == text:
        self.messages[-1].count += 1
    else:
        self.messages.append(Message(text, color))
