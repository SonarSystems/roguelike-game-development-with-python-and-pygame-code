if self.player.is_alive and self.player.level.requires_level_up:
    self.event_handler = LevelUpEventHandler(self)
