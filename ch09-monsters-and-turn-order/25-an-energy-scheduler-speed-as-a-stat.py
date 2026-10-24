def handle_event(self, event):
    action = self.event_handler.handle_event(event)
    if action is None:
        return
    action.perform(self)
    self.turn += 1
    self.run_monster_turns()
    self.update_fov()
