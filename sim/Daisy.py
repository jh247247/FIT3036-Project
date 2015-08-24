
class Daisy:
    MAX_GROWTH = 100
    def __init__(self, parentTile):
        self.growth = 0
        self.living = True
        # TODO: albedo dependent on tile temp/incident radiation?
        # self.albedo =  TODO
        self.age = 0

    def grow(self):
        self.growth += 1

    def update(self):
        """This should be called at every time interval"""
        self.age += 1
        # TODO: Growth dependent on tile incident radiation
        # TODO: Death dependent on age and temp at tile

    def die(self):
        self.living = False

