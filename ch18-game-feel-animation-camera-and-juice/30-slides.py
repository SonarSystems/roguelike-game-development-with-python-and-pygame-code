def visual_position(self, entity):
    slide = self.slides.get(id(entity))
    if slide is None:
        return entity.x, entity.y
    from_x, from_y, to_x, to_y, elapsed = slide
    t = ease_out(min(1.0, elapsed / MOVE_TIME))
    return from_x + (to_x - from_x) * t, from_y + (to_y - from_y) * t
