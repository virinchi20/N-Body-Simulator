import math
class Body:
    
    def __init__(self, position, mass, velocity):
        self.position = position
        self.velocity = velocity
        self.mass = mass

        #self.radius = max(2, math.sqrt(mass) * 0.5)
        self.radius = 1
