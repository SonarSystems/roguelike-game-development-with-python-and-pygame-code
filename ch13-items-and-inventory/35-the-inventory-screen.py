class InventoryDropHandler(InventoryEventHandler):
    TITLE = "Drop which item?"

    def on_item_selected(self, item):
        return DropAction(self.engine.player, item)
