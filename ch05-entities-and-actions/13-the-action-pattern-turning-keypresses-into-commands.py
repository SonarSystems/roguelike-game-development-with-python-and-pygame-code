class Action:
    def __init__(self, entity):
        self.entity = entity

    def perform(self, engine):
        """Carry out the action. Subclasses must override this."""
        raise NotImplementedError()
