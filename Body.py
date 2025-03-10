import math
class Body:
    
    def __init__(self, position, mass, velocity):
        self.x = position[0]
        self.y = position[1]
        self.position = [self.x, self.y]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.ax = 0
        self.ay = 0
        self.mass = mass
        #self.radius = max(3, min(20, int(math.log(mass) * 2)))
        self.color = "blue" if mass < 100 else "yellow" if mass < 140 else "red"
        #self.radius = max(2, math.sqrt(mass) * 0.5)
        self.radius = 1
    
    def update_velocity(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def update_position(self, dt, screen):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < 0: self.x += screen.get_width()
        if self.X > screen.get_width(): self.x -= screen.get_width()
        if self.y < 0: self.y += screen.get_height()
        if self.y > self.get_height(): self.y -= screen.get_height()

    

    
