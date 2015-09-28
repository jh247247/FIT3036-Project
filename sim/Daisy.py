import random

class Daisy:
    def __init__(self, parentTile, albedo, optTemp):
        self.living = True
        self.albedo = albedo
        self.optTemp = optTemp
        self.parent = parentTile

    def update(self):
        """This should be called at every time interval"""
        # TODO: Growth dependent on tile incident radiation
        # TODO: Death dependent on age and temp at tile
        # TODO: death dependent on things other than age...
        chance = 0.0032625*(self.optTemp - self.parent.temp)**2
        if chance > 1 or chance > random.random():
           self.living = False
