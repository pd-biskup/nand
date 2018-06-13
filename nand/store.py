class ChipStore:

    def __init__(self):
        self.store = {}

    def register(self, name, chip):
        if name not in self.store:
            self.store[name] = chip
        else:
            raise KeyError

    def get(self, chip_name, name):
        if chip_name in self.store:
            return self.store[chip_name].build(name)

    def __contains__(self, item):
        return item in self.store

store = ChipStore()
