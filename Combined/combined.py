import math
import pygame
import sys
import os
import time
import random
import numpy as np
from numba import cuda
import numba as nb
from Body import Body
from Rectangle import Rectangle
from QuadTree import QuadTree

# Configuration parameters
BLOCK_SIZE = 256  # Threads per block
TILE_SIZE = 256   # Size of tiles for shared memory

@cuda.jit
def direct_sum_kernel(positions, masses, accelerations, softening, G, num_bodies):
    """
    CUDA kernel for direct sum n-body simulation using tiling approach
    
    Each thread computes forces for one body, utilizing shared memory
    for efficient data access patterns.
    """
    # Shared memory for the tile of positions and masses
    shared_positions = cuda.shared.array(shape=(TILE_SIZE, 2), dtype=nb.float32)
    shared_masses = cuda.shared.array(shape=TILE_SIZE, dtype=nb.float32)
    
    # Get thread and block indices
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    
    # Global thread index
    i = bx * BLOCK_SIZE + tx
    
    # Skip if this thread doesn't correspond to a body
    if i >= num_bodies:
        return
    
    # Local copies of body i's position and accumulator for acceleration
    pos_i_x = positions[i][0]
    pos_i_y = positions[i][1]
    acc_x = 0.0
    acc_y = 0.0
    
    # Loop over tiles
    for tile_start in range(0, num_bodies, TILE_SIZE):
        tile_end = min(tile_start + TILE_SIZE, num_bodies)
        
        # Load tile data into shared memory
        if tile_start + tx < num_bodies:
            shared_positions[tx][0] = positions[tile_start + tx][0]
            shared_positions[tx][1] = positions[tile_start + tx][1]
            shared_masses[tx] = masses[tile_start + tx]
        
        # Synchronize to make sure all threads have loaded the data
        cuda.syncthreads()
        
        # Compute interactions with bodies in this tile
        for j in range(tile_end - tile_start):
            # Skip self-interaction
            if tile_start + j != i:
                # Calculate distance
                dx = shared_positions[j][0] - pos_i_x
                dy = shared_positions[j][1] - pos_i_y
                distance_squared = dx*dx + dy*dy + softening*softening
                distance = math.sqrt(distance_squared)
                
                # Calculate gravitational force
                if distance > 0:
                    f = G * shared_masses[j] / distance_squared
                    acc_x += f * dx / distance
                    acc_y += f * dy / distance
        
        # Synchronize before loading the next tile
        cuda.syncthreads()
    
    # Store the final acceleration
    accelerations[i][0] = acc_x
    accelerations[i][1] = acc_y




def start():
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 1000, 800
    SOFTENING = 5.0
    G = 1
    THETA = 0.5
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill("black")
    pygame.display.set_caption("N-Body simulation")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    font = pygame.font.SysFont(None, 24)

    origin = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
    space = Rectangle(origin[0], origin[1], screen.get_width()/2, screen.get_height()/2)
    
    # Create bodies
    NUM_BODIES = 1000  # Increased for better demonstration of GPU advantage
    bodies = []
    
    for i in range(NUM_BODIES):
        bodies.append(Body(
            [random.randint(1, screen.get_width()), random.randint(1, screen.get_height())],
            random.randint(1, 1000),
            [0, 0]
        ))
    
    # Prepare GPU arrays
    positions = np.zeros((NUM_BODIES, 2), dtype=np.float32)
    masses = np.zeros(NUM_BODIES, dtype=np.float32)
    accelerations = np.zeros((NUM_BODIES, 2), dtype=np.float32)
    
    # Use for toggle between CPU (Quadtree) and GPU (Direct Sum)
    use_gpu = True
    show_quadtree = False

    
    # Time tracking
    last_time = time.time()
    dt = 0.1
    fps_history = []
    running = True
    
    # Initialize arrays with body data
    for i, body in enumerate(bodies):
        positions[i][0] = body.x
        positions[i][1] = body.y
        masses[i] = body.mass

    while running:
        
        start_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                body = Body(pos, random.randint(1, 150), [0, 0])
                bodies.append(body)
                
                # Resize GPU arrays when adding new bodies
                if use_gpu:
                    NUM_BODIES = len(bodies)
                    new_positions = np.zeros((NUM_BODIES, 2), dtype=np.float32)
                    new_masses = np.zeros(NUM_BODIES, dtype=np.float32)
                    new_accelerations = np.zeros((NUM_BODIES, 2), dtype=np.float32)
                    
                    # Copy old data
                    new_positions[:len(positions)] = positions
                    new_masses[:len(masses)] = masses
                    
                    # Update the new arrays with the new body
                    new_positions[len(positions)][0] = body.x
                    new_positions[len(positions)][1] = body.y
                    new_masses[len(masses)] = body.mass
                    
                    # Update arrays
                    positions = new_positions
                    masses = new_masses
                    accelerations = new_accelerations
                    
            if event.type == pygame.KEYDOWN:
                if not use_gpu:
                    if event.key == pygame.K_q:
                        show_quadtree = not show_quadtree
                if event.key == pygame.K_g:
                    if use_gpu:
                        n_bodies = len(bodies)
                    elif not use_gpu:
                        bodies = bodies[:n_bodies]
                    use_gpu = not use_gpu
                    print(f"Using {'GPU' if use_gpu else 'CPU'}")
                    
                    
                
        screen.fill("black")

        if use_gpu:
            # Update GPU arrays with current body data
            for i, body in enumerate(bodies):
                positions[i][0] = body.x
                positions[i][1] = body.y
                masses[i] = body.mass
            
            # Calculate grid and block sizes
            num_blocks = (NUM_BODIES + BLOCK_SIZE - 1) // BLOCK_SIZE
            
            # Address the warning about low occupancy by increasing minimum block count
            if num_blocks < 8:
                num_blocks = 8  # Ensure at least 8 blocks for better GPU utilization
            
            # Execute kernel
            d_positions = cuda.to_device(positions)
            d_masses = cuda.to_device(masses)
            d_accelerations = cuda.to_device(accelerations)
            
            direct_sum_kernel[(num_blocks,), (BLOCK_SIZE,)](
                d_positions, d_masses, d_accelerations, SOFTENING, G, NUM_BODIES
            )
            
            # Copy results back
            d_accelerations.copy_to_host(accelerations)
            
            # Update bodies with calculated accelerations
            for i, body in enumerate(bodies):
                body.ax = accelerations[i][0]
                body.ay = accelerations[i][1]
                
        else:
            # Use the original quadtree method
            qt = QuadTree(space, screen)
            for body in bodies:
                qt.insert(body)

            for body in bodies:
                fx, fy = body.calculate_force(qt, SOFTENING, THETA, G)
                body.ax = fx/body.mass
                body.ay = fy/body.mass
                
            if show_quadtree:
                qt.draw(screen)

        # Update position and velocity for all bodies
        for body in bodies:
            body.update_velocity(dt)
            body.update_position(dt, screen)
            
            # Fix for TypeError: Make sure coordinates are float
            pos = (float(body.x), float(body.y))
            pygame.draw.circle(screen, body.color, pos, body.radius)

        # Calculate and display FPS
        frame_time = time.time() - start_time
        fps = 1.0/max(frame_time, 0.001)
        fps_history.append(fps)
        if len(fps_history) > 30:
            fps_history.pop(0)
        avg_fps = sum(fps_history)/len(fps_history)

        if use_gpu:
            text = "Direct-Sum tiling method on GPU"
        else:
            text = "Barnes-Hut CPU"
        
        
        text_surface = font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 20))
        screen.blit(text_surface, text_rect)

        instructions = [
            "Click: Add Particle",
            "G: switch direct-sum tiling GPU/Barneshut CPU",
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