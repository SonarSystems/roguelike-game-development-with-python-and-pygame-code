def on_player_death(self):
    from ember.savegame import delete_save
    delete_save()                      # permadeath: there is no going back
    self.event_handler = GameOverEventHandler(self)
