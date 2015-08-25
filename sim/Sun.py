
class Sun:
    def __init__(self):
        # radiation value of 1 means that if albedo is 0.5,
        # temperature should eventually become 22.5
        self.radiation = 1

    def update(self):
        self.radiation += 0.001
        print("SunRad: " + str(self.radiation))
        # TODO: make radiation an actual equation that takes in time
