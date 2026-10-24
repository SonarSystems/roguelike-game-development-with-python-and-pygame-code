# file: ember/actions.py
"""Actions: every change to the game world is an Action object.

Input handlers turn keypresses into actions; the engine performs them.
Keeping the two apart means monsters (and, later, tests) can use exactly
the same actions the player does.
"""


class Action:
    def __init__(self, entity):
        self.entity = entity

    def perform(self, engine):
        """Carry out the action. Subclasses must override this."""
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine):
        raise SystemExit()


class WaitAction(Action):
    def perform(self, engine):
        pass  # doing nothing still uses up a turn


class ActionWithDirection(Action):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def destination(self):
        return self.entity.x + self.dx, self.entity.y + self.dy


class MeleeAction(ActionWithDirection):
    def perform(self, engine):
        target = engine.blocking_entity_at(*self.destination)
        if target is None:
            return
        # Real combat arrives in Chapter 11; for now, just report the bump.
        engine.message = f"{self.entity.name} bumps into {target.name}."


class MovementAction(ActionWithDirection):
    def perform(self, engine):
        dest_x, dest_y = self.destination
        if not engine.game_map.is_walkable(dest_x, dest_y):
            return  # bumped into a wall: nothing happens
        if engine.blocking_entity_at(dest_x, dest_y):
            return  # something is standing there
        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """Move if the way is clear; attack if something is standing there."""

    def perform(self, engine):
        if engine.blocking_entity_at(*self.destination):
            return MeleeAction(self.entity, self.dx, self.dy).perform(engine)
        return MovementAction(self.entity, self.dx, self.dy).perform(engine)
