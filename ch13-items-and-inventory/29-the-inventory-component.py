class Inventory:
    """A bag of item entities, with a fixed number of slots."""

    def __init__(self, capacity):
        self.entity = None
        self.capacity = capacity
        self.items = []

    @property
    def is_full(self):
        return len(self.items) >= self.capacity
