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
