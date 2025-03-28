import pygame
import sys
import os
import time
import random
from Body import Body
from Rectangle import Rectangle
from QuadTree import QuadTree
from dotenv import load_dotenv



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
    
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                body = Body(pygame.mouse.get_pos(), random.randint(1, 150), [0, 0])
                bodies.append(body)
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