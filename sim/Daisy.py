import random

class Daisy:
    def __init__(self, parentTile, albedo, optTemp, img):
        self.living = True
        self.albedo = albedo
        self.optTemp = optTemp
        self.parent = parentTile
        self.age = 0
        self.img = img

    def update(self):
        """This should be called at every time interval"""
        # TODO: Growth dependent on tile incident radiation
        # TODO: Death dependent on age and temp at tile
        # TODO: death dependent on things other than age...
        self.age += 1
        chance = 1-0.0032625*((self.optTemp - self.parent.temp)**2)
        val = random.random()
        if val > chance:
            self.living = False
