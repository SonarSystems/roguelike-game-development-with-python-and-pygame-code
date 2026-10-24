def on_player_death(self):
    self.event_handler = GameOverEventHandler(self)
