import pygame
class QuadTree:
    
    def __init__(self, boundary):
        self.boundary = boundary
    
    def draw(self, screen):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
    
        pygame.draw.line(screen, "blue", (x-w, y-h), (x+w, y-h), 5)
        pygame.draw.line(screen, "blue", (x-w, y+h), (x+w, y+h), 5)
        pygame.draw.line(screen, "blue", (x-w, y-h), (x-w, y+h), 5)
        pygame.draw.line(screen, "blue", (x+w, y-h), (x+w, y+h), 5)
