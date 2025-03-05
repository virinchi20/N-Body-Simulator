import pygame
from Rectangle import Rectangle
class QuadTree:
    
    def __init__(self, boundary, screen):
        self.boundary = boundary
        self.capacity = 1
        self.bodies = []
        self.divided = False
        self.screen = screen
        self.draw(screen)
        
    
    def draw(self, screen):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
    
        pygame.draw.line(screen, "blue", (x-w, y-h), (x+w, y-h), 2)
        pygame.draw.line(screen, "blue", (x-w, y+h), (x+w, y+h), 2)
        pygame.draw.line(screen, "blue", (x-w, y-h), (x-w, y+h), 2)
        pygame.draw.line(screen, "blue", (x+w, y-h), (x+w, y+h), 2)

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

        if(self.boundary.contains(body) == False):
            return

        if len(self.bodies) < self.capacity:
            self.bodies.append(body)
        else:
            if not self.divided:
                self.subdivide()        

            self.northeast.insert(body)
            self.northwest.insert(body)
            self.southeast.insert(body)
            self.southwest.insert(body)


                
