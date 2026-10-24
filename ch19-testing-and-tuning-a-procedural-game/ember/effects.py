# file: ember/effects.py
"""Visual-only effects: smooth movement, hit flashes, damage numbers, screen shake.

Nothing here changes the game's rules. The real positions and hit points
live on the entities; these effects just make the changes easy to see.
"""
import random

MOVE_TIME = 0.08        # seconds to slide from one cell to the next
FLASH_TIME = 0.15       # seconds an entity flashes white after being hit
FLOAT_TIME = 0.7        # seconds a damage number stays on screen
FLOAT_RISE = 1.2        # cells a damage number rises over its lifetime
MAX_SHAKE = 8           # pixels of shake at full trauma
TRAUMA_DECAY = 1.8      # trauma lost per second


def ease_out(t):
    """Fast at the start, gentle at the end: feels snappier than linear."""
    return 1 - (1 - t) ** 3


class Effects:
    def __init__(self):
        self.reset()

    def reset(self):
        """Forget everything, e.g. when moving to a new floor."""
        self.slides = {}        # id(entity) -> [from_x, from_y, to_x, to_y, elapsed]
        self.flashes = {}       # id(entity) -> seconds left
        self.floaters = []      # [text, colour, x, y, age]
        self.trauma = 0.0       # 0..1, how hard the screen is shaking

    # -------- events
    def on_damage(self, entity, amount, is_player):
        self.flashes[id(entity)] = FLASH_TIME
        color = (255, 90, 90) if is_player else (255, 230, 120)
        self.floaters.append([str(amount), color, entity.x, entity.y, 0.0])
        if is_player:
            self.trauma = min(1.0, self.trauma + 0.15 + amount * 0.04)

    # -------- per frame
    def update(self, dt, entities):
        for entity in entities:
            slide = self.slides.get(id(entity))
            if slide is None:
                self.slides[id(entity)] = [entity.x, entity.y, entity.x, entity.y, MOVE_TIME]
            elif (slide[2], slide[3]) != (entity.x, entity.y):
                # The entity has moved: start a new slide from where it is drawn now.
                from_x, from_y = self.visual_position(entity)
                self.slides[id(entity)] = [from_x, from_y, entity.x, entity.y, 0.0]
            else:
                slide[4] = min(MOVE_TIME, slide[4] + dt)
        for key in list(self.flashes):
            self.flashes[key] -= dt
            if self.flashes[key] <= 0:
                del self.flashes[key]
        for floater in self.floaters:
            floater[4] += dt
        self.floaters = [f for f in self.floaters if f[4] < FLOAT_TIME]
        self.trauma = max(0.0, self.trauma - TRAUMA_DECAY * dt)

    def visual_position(self, entity):
        slide = self.slides.get(id(entity))
        if slide is None:
            return entity.x, entity.y
        from_x, from_y, to_x, to_y, elapsed = slide
        t = ease_out(min(1.0, elapsed / MOVE_TIME))
        return from_x + (to_x - from_x) * t, from_y + (to_y - from_y) * t

    def is_flashing(self, entity):
        return id(entity) in self.flashes

    def shake_offset(self):
        # Squaring trauma makes small hits subtle and big hits dramatic.
        amount = MAX_SHAKE * self.trauma ** 2
        return random.uniform(-amount, amount), random.uniform(-amount, amount)

    def draw_floaters(self, surface, font, camera, offset):
        for text, color, x, y, age in self.floaters:
            t = age / FLOAT_TIME
            px, py = camera.to_pixels(x + 0.5, y - FLOAT_RISE * t)
            image = font.render(text, True, color)
            image.set_alpha(int(255 * (1 - t)))
            surface.blit(image, image.get_rect(center=(px + offset[0], py + offset[1])))
