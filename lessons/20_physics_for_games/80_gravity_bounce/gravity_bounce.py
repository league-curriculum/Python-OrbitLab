"""
Gravity Bounce with Paddle

A simplified version without classes that includes a movable paddle.
The ball bounces around the screen with gravity, and there's a paddle
at the bottom that can be moved with arrow keys.

"""

import pygame
import sys
from dataclasses import dataclass

@dataclass
class Settings:
    # Screen settings
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    
    # Colors
    WHITE: tuple = (255, 255, 255)
    RED: tuple = (255, 0, 0)
    BLACK: tuple = (0, 0, 0)
    
    # Ball properties
    BALL_RADIUS: int = 20
    INITIAL_VELOCITY_X: int = 5
    INITIAL_VELOCITY_Y: int = 0


    # Paddle properties
    PADDLE_WIDTH: int = 100
    PADDLE_HEIGHT: int = 15
    PADDLE_SPEED: int = 8
    
    # Physics constants
    GRAVITY: float = 0.5
    BOUNCE_DAMPING: float = 0.8
    D_T: float = 1.0  # Time step for physics calculations


# Create settings instance
settings = Settings()

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Bounce with Paddle")
clock = pygame.time.Clock()

# Ball properties
ball_x = settings.SCREEN_WIDTH // 2
ball_y = 50
velocity_x = settings.INITIAL_VELOCITY_X
velocity_y = settings.INITIAL_VELOCITY_Y

# Paddle properties
paddle_x = settings.SCREEN_WIDTH // 2 - settings.PADDLE_WIDTH // 2
paddle_y = settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT

vm = 0
# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= settings.PADDLE_SPEED * settings.D_T

    if keys[pygame.K_RIGHT] and paddle_x < settings.SCREEN_WIDTH - settings.PADDLE_WIDTH:
        paddle_x += settings.PADDLE_SPEED * settings.D_T
    
    # Apply gravity
    velocity_y += settings.GRAVITY * settings.D_T
    
    # Update ball position
    ball_x += velocity_x * settings.D_T
    ball_y += velocity_y * settings.D_T
    
    # Bounce off walls (left and right)
    if ball_x - settings.BALL_RADIUS <= 0 or ball_x + settings.BALL_RADIUS >= settings.SCREEN_WIDTH:
        velocity_x = -velocity_x
        ball_x = max(settings.BALL_RADIUS, min(ball_x, settings.SCREEN_WIDTH - settings.BALL_RADIUS))
    
    # Bounce off floor
    if ball_y + settings.BALL_RADIUS >= settings.SCREEN_HEIGHT:
        ball_y = settings.SCREEN_HEIGHT - settings.BALL_RADIUS
        velocity_y = -velocity_y * settings.BOUNCE_DAMPING
        
        # Stop tiny bounces
        if abs(velocity_y) < 1:
            velocity_y = 0
    
    # Check collision with paddle (detection only, no response)
    if (ball_x + settings.BALL_RADIUS >= paddle_x and 
        ball_x - settings.BALL_RADIUS <= paddle_x + settings.PADDLE_WIDTH and
        ball_y + settings.BALL_RADIUS >= paddle_y and 
        ball_y - settings.BALL_RADIUS <= paddle_y + settings.PADDLE_HEIGHT):

        # Collision detected - no code executed yet
        pass
    


    # Clear screen
    screen.fill(settings.WHITE)
    
    # Draw ball
    pygame.draw.circle(screen, settings.RED, (int(ball_x), int(ball_y)), settings.BALL_RADIUS)
    
    # Draw paddle
    pygame.draw.rect(screen, settings.BLACK, (int(paddle_x), int(paddle_y), settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit
pygame.quit()
sys.exit()
