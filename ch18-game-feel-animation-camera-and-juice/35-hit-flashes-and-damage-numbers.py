def draw_floaters(self, surface, font, camera, offset):
    for text, color, x, y, age in self.floaters:
        t = age / FLOAT_TIME
        px, py = camera.to_pixels(x + 0.5, y - FLOAT_RISE * t)
        image = font.render(text, True, color)
        image.set_alpha(int(255 * (1 - t)))
        surface.blit(image, image.get_rect(center=(px + offset[0], py + offset[1])))
