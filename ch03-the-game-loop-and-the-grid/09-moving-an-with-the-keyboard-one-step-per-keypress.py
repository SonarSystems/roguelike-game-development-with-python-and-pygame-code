dx, dy = MOVE_KEYS[event.key]
new_x, new_y = player_x + dx, player_y + dy
if 0 <= new_x < settings.GRID_WIDTH and 0 <= new_y < settings.GRID_HEIGHT:
    player_x, player_y = new_x, new_y
    turns += 1
