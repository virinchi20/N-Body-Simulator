class Body:
    def __init__(self, position, mass, velocity):
        self.x = float(position[0])
        self.y = float(position[1])
        self.position = [self.x, self.y]
        self.vx = float(velocity[0])
        self.vy = float(velocity[1])
        self.ax = 0.0
        self.ay = 0.0
        self.mass = float(mass)
        self.color = "blue" if mass < 100 else "yellow" if mass < 140 else "red"
        self.radius = 1
    
    def update_velocity(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def update_position(self, dt, screen):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < 0: self.x += screen.get_width()
        if self.x > screen.get_width(): self.x -= screen.get_width()
        if self.y < 0: self.y += screen.get_height()
        if self.y > screen.get_height(): self.y -= screen.get_height()
        
        # Update position list as well
        self.position[0] = self.x
        self.position[1] = self.y
