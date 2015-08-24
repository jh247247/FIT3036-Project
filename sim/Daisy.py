import random

class Daisy:
    MAX_GROWTH = 100
    def __init__(self, parentTile, albedo):
        self.growth = 0
        self.living = True
        self.albedo = albedo
        self.age = 0

    def grow(self):
        self.growth += 1

    def update(self):
        """This should be called at every time interval"""
        self.age += 1
        # TODO: Growth dependent on tile incident radiation
        # TODO: Death dependent on age and temp at tile
        # TODO: death dependent on things other than age...
        if self.age/100 > random.random():
            self.die()

    def die(self):
        self.living = False

