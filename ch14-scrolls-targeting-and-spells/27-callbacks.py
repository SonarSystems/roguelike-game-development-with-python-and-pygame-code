engine.event_handler = SingleTargetHandler(
    engine, lambda cell: ItemAction(user, self.entity, cell))
