import pygame
import sys
import os
import time
import random
from Body import Body
from Rectangle import Rectangle
from QuadTree import QuadTree



def start():

    #pygame window parameters
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Space")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    origin = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

    space = Rectangle(origin[0], origin[1], screen.get_width()/2, screen.get_height()/2)
    #qt = QuadTree(space)
    #qt.subdivide()
    #print(qt.northeast.x)
    

    #body_pos = origin

    bodies = []
    #for i in range(1000):
    #    bodies.append(Body([random.randint(1, screen.get_width()), random.randint(1, screen.get_height())], random.randint(1,1000), [0, 0]))

    screen.fill("black")
    qt = QuadTree(space, screen)
    running = True

    while running:

        
        qt.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                #print(pos[0]+10)
                body = Body(pygame.mouse.get_pos(), random.randint(1, 1000), [0, 0])
                bodies.append(body)
                qt.insert(body)
                pygame.draw.circle(screen, body.color, body.position, body.radius)
                

        

        
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        #pygame.draw.circle(screen, "white", body_pos, 1)
        for i in range(len(bodies)):
            pygame.draw.circle(screen, "white", bodies[i].position, bodies[i].radius)
            qt.insert(bodies[i])
        """
        #qt.draw(screen)

        pygame.display.flip()

        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    start()