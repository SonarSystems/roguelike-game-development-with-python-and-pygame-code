def die(self, engine):
    entity = self.entity
    if entity is engine.player:
        engine.log("You die...", settings.DEATH_RED)
        engine.on_player_death()
    else:
        engine.log(f"The {entity.name} dies.", settings.ORANGE)
    entity.char = "%"
    entity.color = settings.CORPSE_RED
    entity.blocks_movement = False
    entity.ai = None
    entity.name = f"remains of {entity.name}"
    entity.render_order = 0      # corpses are drawn underneath the living
