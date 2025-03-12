import pygame
from Rectangle import Rectangle
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
            

            
            
            
            


                
