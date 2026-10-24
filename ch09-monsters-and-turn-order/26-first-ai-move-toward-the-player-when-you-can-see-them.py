class BaseAI:
    def __init__(self, entity):
        self.entity = entity

    def decide(self, engine):
        """Return the Action this entity should perform."""
        raise NotImplementedError()
