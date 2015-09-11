import random

class Daisy:
    MAX_GROWTH = 100
    TEMP_FUDGE = 0.01
    # TODO: add optimal temps for types of daisy
    def __init__(self, parentTile, albedo, optTemp):
        self.growth = 0
        self.living = True
        self.albedo = albedo
        self.age = 0
        self.optTemp = optTemp
        self.parent = parentTile

    def grow(self):
        self.growth += 1

    def update(self):
        """This should be called at every time interval"""
        self.age += 1
        # TODO: Growth dependent on tile incident radiation
        # TODO: Death dependent on age and temp at tile
        # TODO: death dependent on things other than age...
        if self.age/self.MAX_GROWTH + \
           abs(self.parent.temp-self.optTemp)*self.TEMP_FUDGE \
           > random.random():
            self.die()

    def die(self):
        self.living = False
