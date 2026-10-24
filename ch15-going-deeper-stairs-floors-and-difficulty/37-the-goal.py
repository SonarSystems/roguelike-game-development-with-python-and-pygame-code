class VictoryConsumable(Consumable):
    """The Ember Crown: using it ends the run in victory."""

    def activate(self, user, engine, target=None):
        engine.log("You raise the Ember Crown. Its light carries you to the surface!",
                   settings.EMBER)
        engine.on_victory()
