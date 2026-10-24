import pygame

class LevelUpEventHandler(EventHandler):
    """Shown when the player has enough XP: pick one improvement."""

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        level = self.engine.player.level
        choice = {pygame.K_a: level.increase_max_hp, pygame.K_b: level.increase_power,
                  pygame.K_c: level.increase_defense}.get(event.key)
        if choice is None:
            return None      # a choice is required: ignore other keys
        choice()
        if not level.requires_level_up:
            self.engine.event_handler = MainGameEventHandler(self.engine)
        return None

    def on_render(self, surface, glyphs):
        fighter = self.engine.player.fighter
        lines = ["Congratulations! Choose a stat to raise:",
                 f"(a) Constitution  +20 HP   (now {fighter.max_hp})",
                 f"(b) Strength      +1 power (now {fighter.power})",
                 f"(c) Agility       +1 defense (now {fighter.defense})"]
        draw_box(surface, glyphs, f"Level {self.engine.player.level.current_level + 1}!",
                 lines, 2, 2, 30)
