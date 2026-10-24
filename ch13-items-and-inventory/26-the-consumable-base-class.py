class HealingConsumable(Consumable):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, user, engine, target=None):
        recovered = user.fighter.heal(self.amount)
        if recovered == 0:
            raise Impossible("Your health is already full.")
        engine.log(f"You drink the {self.entity.name} and recover {recovered} HP.",
                   settings.HEALED_GREEN)
        self.consume(user)
