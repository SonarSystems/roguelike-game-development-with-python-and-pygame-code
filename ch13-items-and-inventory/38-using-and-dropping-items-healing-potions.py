class DropAction(ItemAction):
    def perform(self, engine):
        actor, item = self.entity, self.item
        actor.inventory.items.remove(item)
        item.x, item.y = actor.x, actor.y
        engine.entities.insert(0, item)
        engine.log(f"You drop the {item.name}.")
