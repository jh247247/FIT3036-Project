
class Tile:
    def __init__(self, parentWorld):
        self.parent = parentWorld
        # TODO: Make different types of object that occupy this tile
        self.obj = None
        # TODO: get temperature from parent world

    def update(self):
        # TODO: update temp based on incoming incident radiation
        if self.obj is not None:
            self.obj.update()

    def draw(self):
        i = 0
        # TODO: figure out how to redraw to a given canvas, should we
        # pass in coords?
