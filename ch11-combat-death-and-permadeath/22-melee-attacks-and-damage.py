class MeleeAction(ActionWithDirection):
    def perform(self, engine):
        target = engine.blocking_entity_at(*self.destination)
        if target is None or target.fighter is None:
            return
        attacker = self.entity
        damage = attacker.fighter.power - target.fighter.defense
        description = f"{attacker.name} attacks {target.name}"
        color = settings.PLAYER_ATTACK if attacker is engine.player else settings.ENEMY_ATTACK
        if damage > 0:
            engine.log(f"{description} for {damage} hit points.", color)
            target.fighter.take_damage(damage, engine)
        else:
            engine.log(f"{description} but does no damage.", color)
