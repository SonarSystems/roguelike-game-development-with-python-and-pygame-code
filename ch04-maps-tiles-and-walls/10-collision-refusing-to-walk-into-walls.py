dx, dy = MOVE_KEYS[event.key]
new_x, new_y = player_x + dx, player_y + dy
if game_map.is_walkable(new_x, new_y):
    player_x, player_y = new_x, new_y
    turns += 1
