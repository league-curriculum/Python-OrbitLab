"""
Gravity Bounce 

If we add X velocity, from side to side, the player will bounce around the
screen. We will need to add a check to see if the player hits the left or right
side of the screen.

uid: IaZqWmy2
name: Gravity Bounce
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Bounce")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_x = SCREEN_WIDTH // 2
ball_y = 50
ball_radius = 20
velocity_x = 5
velocity_y = 0

# Physics constants
GRAVITY = 0.5
BOUNCE_DAMPING = 0.8
D_T = 1.0  # Time step for physics calculations

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Apply gravity
    velocity_y += GRAVITY * D_T
    
    # Update ball position
    ball_x += velocity_x * D_T
    ball_y += velocity_y * D_T
    
    # Bounce off walls (left and right)
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= SCREEN_WIDTH:
        velocity_x = -velocity_x
        ball_x = max(ball_radius, min(ball_x, SCREEN_WIDTH - ball_radius))
    
    # Bounce off floor
    if ball_y + ball_radius >= SCREEN_HEIGHT:
        ball_y = SCREEN_HEIGHT - ball_radius
        velocity_y = -velocity_y * BOUNCE_DAMPING
        
        # Stop tiny bounces
        if abs(velocity_y) < 1:
            velocity_y = 0
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit
pygame.quit()
sys.exit()
