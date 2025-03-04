import pygame
from Rectangle import Rectangle
class QuadTree:
    
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.bodies = []
        self.divided = False
    
    def draw(self, screen):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
    
        pygame.draw.line(screen, "blue", (x-w, y-h), (x+w, y-h), 5)
        pygame.draw.line(screen, "blue", (x-w, y+h), (x+w, y+h), 5)
        pygame.draw.line(screen, "blue", (x-w, y-h), (x-w, y+h), 5)
        pygame.draw.line(screen, "blue", (x+w, y-h), (x+w, y+h), 5)

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x+w/2, y+h/2, w/2, h/2)
        self.northeast = QuadTree(ne)
        nw = Rectangle(x-w/2, y+h/2, w/2, h/2)
        self.northwest = QuadTree(nw)
        se = Rectangle(x+w/2, y-h/2, w/2, h/2)
        self.southeast = QuadTree(se)
        sw = Rectangle(x-w/2, y-h/2, w/2, h/2)
        self.southwest = QuadTree(sw)

    def insert(self, body):

        if(not self.boundary.contains(body)):
            return

        if len(self.bodies) < self.capacity:
            self.bodies.push(body)
        else:
            if not self.divided:
                self.subdivide()
                self.divided = True

                
