def increase_max_hp(self, amount=20):
    fighter = self.entity.fighter
    fighter.max_hp += amount
    fighter.hp += amount
    self.increase_level()
