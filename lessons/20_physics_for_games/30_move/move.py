"""
Moving Square

Move the square with the arrow keys. That's it.
Everything happens in one loop so it's easy to follow.


"""

import pygame

# Basic settings
WIDTH = 600
HEIGHT = 600
SIZE = 50  # Square size in pixels
D_X = 5  # Pixels per frame (simple, not time-based)

# Colors (R, G, B)
BACKGROUND = (255, 255, 255)      # White
SQUARE_COLOR = (150, 200, 255)    # Light blue

# Initialize pygame and the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Square")
clock = pygame.time.Clock()
FPS = 60  # Frames per second (keeps things from running too fast)

# Start in the center
x = WIDTH // 2 - SIZE // 2
y = HEIGHT // 2 - SIZE // 2

running = True
while running:
    # Handle events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key state (which keys are held down)
    keys = pygame.key.get_pressed()

    # Update position
    if keys[pygame.K_LEFT]:
        x -= D_X
    if keys[pygame.K_RIGHT]:
        x += D_X
    if keys[pygame.K_UP]:
        y -= D_X
    if keys[pygame.K_DOWN]:
        y += D_X

    # Keep square on screen
    x = max(0, min(WIDTH - SIZE, x))
    y = max(0, min(HEIGHT - SIZE, y))

    # Draw
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, SQUARE_COLOR, (x, y, SIZE, SIZE))
    pygame.display.flip()

    # Slow the loop to ~FPS frames per second
    clock.tick(FPS)

pygame.quit()
