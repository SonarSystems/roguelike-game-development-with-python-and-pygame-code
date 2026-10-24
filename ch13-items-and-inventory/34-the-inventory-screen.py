class InventoryActivateHandler(InventoryEventHandler):
    TITLE = "Use which item?"

    def on_item_selected(self, item):
        return ItemAction(self.engine.player, item)
