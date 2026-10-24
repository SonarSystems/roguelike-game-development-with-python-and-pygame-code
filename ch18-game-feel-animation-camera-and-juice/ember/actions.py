# file: ember/actions.py
"""Actions: every change to the game world is an Action object.

Input handlers turn keypresses into actions; the engine performs them.
Keeping the two apart means monsters (and, later, tests) can use exactly
the same actions the player does.
"""
from ember import settings, tiles
from ember.exceptions import Impossible


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
        if target is None or target.fighter is None:
            return
        attacker = self.entity
        damage = attacker.fighter.power - target.fighter.defense
        description = f"{attacker.name} attacks {target.name}"
        color = settings.PLAYER_ATTACK if attacker is engine.player else settings.ENEMY_ATTACK
        if damage > 0:
            engine.log(f"{description} for {damage} hit points.", color)
            target.fighter.take_damage(damage, engine)
        else:
            engine.log(f"{description} but does no damage.", color)


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


class TakeStairsAction(Action):
    def perform(self, engine):
        x, y = self.entity.x, self.entity.y
        if engine.game_map.tiles[x][y] is not tiles.DOWN_STAIRS:
            raise Impossible("There are no stairs here.")
        engine.game_world.generate_floor(engine)
        engine.log(f"You descend to depth {engine.game_world.depth}.", settings.DESCEND)


class PickupAction(Action):
    """Pick up the item on the player's tile, if there is one."""

    def perform(self, engine):
        actor = self.entity
        for item in engine.entities:
            if item.is_item and item.x == actor.x and item.y == actor.y:
                if actor.inventory.is_full:
                    raise Impossible("Your inventory is full.")
                engine.entities.remove(item)
                actor.inventory.items.append(item)
                engine.log(f"You pick up the {item.name}.")
                return
        raise Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    """Use an item from the inventory, optionally on a target cell."""

    def __init__(self, entity, item, target=None):
        super().__init__(entity)
        self.item = item
        self.target = target

    def perform(self, engine):
        self.item.consumable.activate(self.entity, engine, self.target)


class DropAction(ItemAction):
    def perform(self, engine):
        actor, item = self.entity, self.item
        if actor.equipment and actor.equipment.is_equipped(item):
            actor.equipment.toggle(item, engine)     # take it off before dropping it
        actor.inventory.items.remove(item)
        item.x, item.y = actor.x, actor.y
        engine.entities.insert(0, item)
        engine.log(f"You drop the {item.name}.")


class EquipAction(Action):
    """Equip or remove an item from the inventory. Changing gear takes a turn."""

    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self, engine):
        self.entity.equipment.toggle(self.item, engine)
