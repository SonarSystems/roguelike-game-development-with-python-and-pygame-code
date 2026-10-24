def new_game(seed, kind=None):
    """Start a fresh run. `kind` is accepted for compatibility but every
    floor now picks its own generator from its seed."""
    player = entity_factories.player(0, 0)
    engine = Engine(GameWorld(seed), player)
    engine.log(f"Welcome to Ember Depths. (Seed {seed})", settings.EMBER)
    engine.log("Find the stairs (>) and reach depth 10 for the Ember Crown.", settings.EMBER)
    return engine
