
class Sun:
    def __init__(self):
        # radiation value of 1 means that if albedo is 0.5,
        # temperature should eventually become 22.5
        self.radiation = 1.5

    def update(self):
        self.radiation -= 0.001
        # TODO: make radiation an actual equation that takes in time
