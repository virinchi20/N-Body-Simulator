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
    qt = QuadTree(space)

    #body_pos = origin

    bodies = []
    for i in range(10):
        bodies.append(Body([random.randint(0, screen.get_width()), random.randint(0, screen.get_height())], random.randint(1,1000), [0, 0]))

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        #pygame.draw.circle(screen, "white", body_pos, 1)
        for i in range(len(bodies)):
            pygame.draw.circle(screen, "white", bodies[i].position, bodies[i].radius)

        qt.draw(screen)

        pygame.display.flip()

        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    start()