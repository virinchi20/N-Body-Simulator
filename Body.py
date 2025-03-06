import math
class Body:
    
    def __init__(self, position, mass, velocity):
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.radius = max(3, min(20, int(math.log(mass) * 2)))
        self.color = "blue" if mass < 50 else "yellow" if mass < 500 else "red"
        #self.radius = max(2, math.sqrt(mass) * 0.5)
        #self.radius = 1
    
    def update_velocity(self, dt):
        self.vx += self.ax * dt
        self.vy = self.ay * dt

    

    
