def wander(self, engine):
    # engine.rng, not the global random module: a run must replay
    # exactly from its seed (see Chapter 19).
    if engine.rng.random() < 0.5:
        dx, dy = engine.rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        return MovementAction(self.entity, dx, dy)
    return WaitAction(self.entity)
