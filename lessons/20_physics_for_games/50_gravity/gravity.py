"""
Gravity Jump (Ultra Simple)

One square that keeps auto-jumping with gravity pulling it down.
Upward motion is fast, falling is slower — because velocity changes a little
each frame due to gravity.


"""

import pygame
from orbitlib.colors import Colors

# --- Settings (simple constants) ---
WIDTH = 500
HEIGHT = 500
SIZE = 10
PLAYER_X = 100

JUMP_VELOCITY = 200.0   # pixels / second upward (we'll negate it)
GRAVITY = 60.0          # pixels / second^2 downward
FPS = 30
DT = 1 / FPS            # seconds per frame

BACKGROUND = Colors.WHITE
PLAYER_COLOR = Colors.BLACK

# --- Init pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Jump")
clock = pygame.time.Clock()

# --- Initial state ---
x = PLAYER_X
y = HEIGHT - SIZE           # start on the "ground"
v_y = 0.0                   # vertical velocity
is_jumping = False          # track if we are mid-jump

running = True
while running:
    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Physics ---
    if not is_jumping:
        # Start a jump: give an instant upward velocity
        v_y = -JUMP_VELOCITY   # negative because up is smaller y on screen
        is_jumping = True

    # Gravity accelerates downward (adds to velocity)
    v_y += GRAVITY * DT
    y += v_y * DT

    # Ground collision
    if y + SIZE >= HEIGHT:
        y = HEIGHT - SIZE
        v_y = 0.0
        is_jumping = False    # ready to jump again next frame

    # --- Draw ---
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, PLAYER_COLOR, (x, y, SIZE, SIZE))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
