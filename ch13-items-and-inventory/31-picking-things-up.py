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
