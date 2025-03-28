import math
import pygame
import sys
import os
import time
import random



class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, body):
        body_x = body.x
        body_y = body.y
        return (
            body_x >= self.x - self.w and
            body_x < self.x + self.w and
            body_y >= self.y - self.h and
            body_y < self.y + self.h
        )
    
    
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
        if self.x > screen.get_width(): self.x -= screen.get_width()
        if self.y < 0: self.y += screen.get_height()
        if self.y > screen.get_height(): self.y -= screen.get_height()

    
    def calculate_force(self, qtree, SOFTENING, THETA, G):

        if qtree.total_mass == 0:
            return 0, 0
        
        dx = qtree.center_of_mass[0] - self.x
        dy = qtree.center_of_mass[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy + SOFTENING*SOFTENING)

        s = max(qtree.boundary.x, qtree.boundary.y)
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

class QuadTree:
    
    def __init__(self, boundary, screen):
        self.boundary = boundary
        self.capacity = 1
        self.bodies = []
        self.divided = False
        self.screen = screen
        #self.draw(screen)
        self.total_mass = 0
        self.center_of_mass = [0, 0]
        
    
    def draw(self, screen):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
    
        pygame.draw.line(screen, "blue", (x-w, y-h), (x+w, y-h), 2)
        pygame.draw.line(screen, "blue", (x-w, y+h), (x+w, y+h), 2)
        pygame.draw.line(screen, "blue", (x-w, y-h), (x-w, y+h), 2)
        pygame.draw.line(screen, "blue", (x+w, y-h), (x+w, y+h), 2)
        if self.divided:
            self.northeast.draw(screen)
            self.northwest.draw(screen)
            self.southeast.draw(screen)
            self.southwest.draw(screen)

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x+w/2, y+h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.screen)
        nw = Rectangle(x-w/2, y+h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.screen)
        se = Rectangle(x+w/2, y-h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.screen)
        sw = Rectangle(x-w/2, y-h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.screen)

        self.divided = True

    def insert(self, body):

        if(not self.boundary.contains(body)):
            return False
        

        new_mass = self.total_mass + body.mass
        self.center_of_mass[0] = (self.center_of_mass[0]*self.total_mass + body.x*body.mass)/new_mass
        self.center_of_mass[1] = (self.center_of_mass[1]*self.total_mass + body.y*body.mass)/new_mass
        self.total_mass = new_mass


        #self.total_mass += body.mass
        #self.total_mass = sum(self.bodies.mass)

        if len(self.bodies) < self.capacity and not self.divided:
            self.bodies.append(body)
            return True
        
        if not self.divided:
            self.subdivide()   

            for b in self.bodies:
                if self.northeast.insert(b):
                    pass
                elif self.northwest.insert(b):
                    pass
                elif self.southeast.insert(b):
                    pass
                elif self.southwest.insert(b):
                    pass
            #self.bodies.append(body)
            self.bodies = []
        
        if self.northeast.insert(body):
            return True
        elif self.northwest.insert(body):
            return True
        elif self.southeast.insert(body):
            return True
        elif self.southwest.insert(body):
            return True

        return False
            

            
def start():

    #pygame window parameters
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 1000, 800
    SOFTENING = 5.0
    #G = 6.67430e-11
    G = 1
    THETA = 0.5
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill("black")
    pygame.display.set_caption("2D Space")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    font = pygame.font.SysFont(None, 24)

    origin = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

    space = Rectangle(origin[0], origin[1], screen.get_width()/2, screen.get_height()/2)
    
    #qt = QuadTree(space, screen)
    bodies = []
    
    for i in range(100):
        bodies.append(Body([random.randint(1, screen.get_width()), random.randint(1, screen.get_height())], random.randint(1,1000), [0, 0]))
        #pygame.draw.circle(screen, "white", bodies[i].position, bodies[i].radius)
        #qt.insert(bodies[i])
    
    
    show_quadtree = False

    dt = 0.1
    fps_history = []
    running = True

    while running:

        start_time = time.time()
        
        #qt.draw(screen)
    
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #print(pos)
                #print(pos[0]+10)
                body = Body(pygame.mouse.get_pos(), random.randint(1, 150), [0, 0])
                bodies.append(body)
                #qt.insert(body)
                #qt.draw(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    show_quadtree = not show_quadtree
                
                
        screen.fill("black")

        qt = QuadTree(space, screen)
        for body in bodies:
            qt.insert(body)

        for body in bodies:
            fx, fy = body.calculate_force(qt, SOFTENING, THETA, G)
            body.ax = fx/body.mass
            body.ay = fy/body.mass

        for body in bodies:
            body.update_velocity(dt)
            body.update_position(dt, screen)

        if show_quadtree:
            qt.draw(screen)

        for body in bodies:
            pygame.draw.circle(screen, body.color, [body.x, body.y], body.radius)
        
        #FPS
        frame_time = time.time() - start_time
        fps = 1.0/max(frame_time, 0.001)
        fps_history.append(fps)
        if len(fps_history) > 30:
            fps_history.pop(0)
        avg_fps = sum(fps_history)/len(fps_history)

        #Metrics Display
        instructions = [
            "Click: Add Particle",
            "Q: Show Quadtree",
            f"Bodies: {len(bodies)}",
            f"FPS: {avg_fps:.1f}"
        ]

        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10+25*i))

        pygame.display.flip()

        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    start()
            
            
            


                
