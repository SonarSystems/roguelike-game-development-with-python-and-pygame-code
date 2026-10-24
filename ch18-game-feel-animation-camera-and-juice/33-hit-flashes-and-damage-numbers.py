def on_damage(self, entity, amount, is_player):
    self.flashes[id(entity)] = FLASH_TIME
    color = (255, 90, 90) if is_player else (255, 230, 120)
    self.floaters.append([str(amount), color, entity.x, entity.y, 0.0])
    if is_player:
        self.trauma = min(1.0, self.trauma + 0.15 + amount * 0.04)
