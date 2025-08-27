"""
Acceleration with a Spring

The square is pulled toward the center by a spring-like force.
You can see acceleration change the velocity, and velocity change the position.

uid: 3hb3eMvH
name: Spring Acceleration
"""

import pygame

# Screen
WIDTH = 600
HEIGHT = 600
SIZE = 50

# Physics constants
K = 3.0      # Spring constant (higher = stronger pull)
MASS = 2.0   # Mass (affects how strongly acceleration changes velocity)
FPS = 60
DT = 1 / FPS

# Colors (R,G,B)
BACKGROUND = (0, 0, 0)
SQUARE_COLOR = (255, 0, 0)
CENTER_COLOR = (0, 255, 0)     # Green circle at equilibrium point
LINE_COLOR = (50, 150, 255)     # Blue line showing displacement

# Init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Acceleration (Spring)")
clock = pygame.time.Clock()

# Start a little off-center so motion begins
x = 20.0
y = HEIGHT // 2 - SIZE // 2
v_x = 0.0  # velocity (pixels / second)

center_x = (WIDTH - SIZE) // 2            # equilibrium x position
center_y = (HEIGHT - SIZE) // 2 + SIZE // 2  # y center (circle & line anchor)

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Physics ---

    d = x - center_x               # displacement, how far from center (x only)

    # Hooke's law
    a_x = (-K * d) / MASS          # acceleration (pixels / s^2)
    v_x += a_x * DT                # update velocity
    x += v_x * DT                  # update position

    # --- Draw ---
    screen.fill(BACKGROUND)

    # Draw blue line from center to square center (visualize displacement)
    square_center = (x + SIZE / 2, y + SIZE / 2)
    pygame.draw.line(screen, LINE_COLOR, (center_x + SIZE / 2, center_y), square_center, 3)

    # Draw green center point (equilibrium)
    pygame.draw.circle(screen, CENTER_COLOR, (int(center_x + SIZE / 2), int(center_y)), 8)

    # Draw the moving square last so it sits on top
    pygame.draw.rect(screen, SQUARE_COLOR, (x, y, SIZE, SIZE))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
