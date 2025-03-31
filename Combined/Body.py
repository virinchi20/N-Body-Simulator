import math
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
        self.radius = 1.5
    
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
    
    def calculate_force(self, qtree, SOFTENING, THETA, G):
        if qtree.total_mass == 0:
            return 0, 0
        
        dx = qtree.center_of_mass[0] - self.x
        dy = qtree.center_of_mass[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy + SOFTENING*SOFTENING)

        s = max(qtree.boundary.w, qtree.boundary.h)
        if not qtree.divided or s/distance < THETA:
            if distance > 0:
                f = G * self.mass * qtree.total_mass / (distance * distance)
                fx = f * dx / distance
                fy = f * dy / distance
                return fx, fy
            return 0, 0
        
        fx, fy = 0, 0
        if qtree.northwest:
            qfx, qfy = self.calculate_force(qtree.northwest, SOFTENING, THETA, G)
            fx += qfx
            fy += qfy
        if qtree.northeast:
            qfx, qfy = self.calculate_force(qtree.northeast, SOFTENING, THETA, G)
            fx += qfx
            fy += qfy
        if qtree.southwest:
            qfx, qfy = self.calculate_force(qtree.southwest, SOFTENING, THETA, G)
            fx += qfx
            fy += qfy
        if qtree.southeast:
            qfx, qfy = self.calculate_force(qtree.southeast, SOFTENING, THETA, G)
            fx += qfx
            fy += qfy
    
        return fx, fy