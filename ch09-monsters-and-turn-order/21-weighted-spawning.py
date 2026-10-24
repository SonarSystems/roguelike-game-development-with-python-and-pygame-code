def new_game(seed, kind=None):
    game_map, rooms = generate_level(seed, settings.GRID_WIDTH, MAP_HEIGHT, kind)
    start = rooms[0].center
    player = entity_factories.player(*start)
    monsters = spawn_monsters(seed, game_map, start, MONSTERS_PER_LEVEL)
    return Engine(game_map, player, monsters + [player])
