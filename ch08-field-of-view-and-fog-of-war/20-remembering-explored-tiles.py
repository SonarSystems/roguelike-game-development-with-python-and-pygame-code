def update_fov(self):
    player = self.player
    self.game_map.visible = compute_fov(self.game_map.is_transparent,
                                        player.x, player.y, FOV_RADIUS)
    self.game_map.explored |= self.game_map.visible
