class SingleTargetHandler(SelectCellHandler):
    def __init__(self, engine, callback):
        super().__init__(engine)
        self.callback = callback    # turns the chosen cell into an Action

    def on_selected(self, cell):
        return self.callback(cell)
