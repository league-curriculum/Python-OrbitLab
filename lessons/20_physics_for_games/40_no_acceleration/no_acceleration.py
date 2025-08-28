"""
Automatic Back-and-Forth Motion (No Acceleration)

The square slides left and right at a constant speed and bounces off the
screen edges. No acceleration, no extra abstractions—just a simple loop.


"""

import pygame

# Basic settings (kept small & obvious for students)
WIDTH = 600
HEIGHT = 600
SIZE = 50          # Square side length (pixels)
DX = 5             # Pixels moved each frame (constant speed)
FPS = 60           # Frames per second

# Colors (R, G, B)
BACKGROUND = (0, 0, 0)      # Black
SQUARE_COLOR = (255, 0, 0)  # Red

# Initialize pygame and window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back and Forth (No Acceleration)")
clock = pygame.time.Clock()

# Start at left edge, vertically centered
x = 0
y = HEIGHT // 2 - SIZE // 2
direction = 1  # 1 moves right, -1 moves left

running = True
while running:
    # Handle window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update position
    x += DX * direction

    # Bounce at edges
    if x + SIZE >= WIDTH:
        direction = -1
    elif x <= 0:
        direction = 1

    # Draw frame
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, SQUARE_COLOR, (x, y, SIZE, SIZE))
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

pygame.quit()
