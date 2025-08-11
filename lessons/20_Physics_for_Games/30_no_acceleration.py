"""
Move a square, with no acceleration
"""
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SQUARE_SIZE = 50
SQUARE_COLOR = (255, 0, 0)  # Red
SQUARE_SPEED = 300

FPS = 60  # Frames per second

d_t = 1 / FPS  # Time step for physics calculations

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Red Square")

# Square starting position
x = 0
y = (SCREEN_HEIGHT - SQUARE_SIZE) // 2

# Movement direction: 1 for right, -1 for left
direction = 1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the square, a bit each frame

    d_x = SQUARE_SPEED * direction * d_t

    x += d_x

    # Check for screen bounds and reverse direction if necessary
    if x + SQUARE_SIZE > SCREEN_WIDTH:
        direction = -1  # Move left
    elif x < 0:
        direction = 1  # Move right

    # Fill the screen with black (clears previous frame)
    screen.fill((0, 0, 0))

    # Draw the red square
    pygame.draw.rect(screen, SQUARE_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
