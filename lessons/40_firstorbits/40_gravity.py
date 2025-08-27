"""
Simple Orbital Motion with Basic Physics

This program demonstrates basic orbital motion principles using simple physics equations.
A sun is drawn in the center, and an earth orbits around it using basic velocity and 
position updates - the same math principles as the gravity demo but extended to 2D.

uid: B2e0lLRD
name: Gravity
"""

import pygame
import math
from dataclasses import dataclass
from orbitlib.colors import Colors

# Initialize Pygame
pygame.init()


@dataclass
class GameSettings:
    """Class for keeping track of game settings."""
    screen_width: int = 500
    screen_height: int = 500
    
    # Colors
    white: tuple = Colors.WHITE
    black: tuple = Colors.BLACK
    yellow: tuple = Colors.YELLOW  # Sun color
    blue: tuple = Colors.BLUE      # Earth color
    
    # Physics - same basic principles as before
    d_t: float = 1.0/30  # time step, same as before
    
    # Simple orbital parameters (not full gravitational physics yet)
    # Tripled speed - one orbit takes ~10 seconds at 30 FPS
    orbital_speed: float = 10.5  # how fast earth moves in its orbit (tripled from 3.5)

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Simple Orbital Motion")

# Sun position (just a fixed point in the center)
sun_x = settings.screen_width // 2
sun_y = settings.screen_height // 2
sun_radius = 20

# Earth variables - no objects, just simple variables
earth_radius = 8
orbital_radius = 150  # Distance from sun center

# Earth's position - start to the right of the sun
earth_x = sun_x + orbital_radius
earth_y = sun_y

# Earth's velocity components - using same velocity concept as before
# For circular motion, velocity is perpendicular to radius
earth_vel_x = 0.0           # Start with no horizontal velocity  
earth_vel_y = -settings.orbital_speed  # Start with upward velocity

# Acceleration toward center (centripetal acceleration)
# Using same acceleration concept: a = change in velocity per frame
# Increased significantly to maintain circular orbit at tripled speed
centripetal_acceleration = 1.08  # Increased by factor of 9 (speed squared)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate direction from earth to sun (for centripetal acceleration)
    # Distance components
    d_x = sun_x - earth_x
    d_y = sun_y - earth_y
    
    # Distance (using math.sqrt for distance calculation)
    distance = math.sqrt(d_x * d_x + d_y * d_y)
    
    # Unit vector pointing toward sun (normalized direction)
    if distance > 0:
        unit_x = d_x / distance
        unit_y = d_y / distance
    else:
        unit_x = unit_y = 0
    
    # Acceleration toward sun (same concept as gravity acceleration before)
    # a = acceleration toward center
    a_x = unit_x * centripetal_acceleration
    a_y = unit_y * centripetal_acceleration
    
    # Update velocity using acceleration (same as: d_v_y += a_y * d_t)
    earth_vel_x += a_x * settings.d_t
    earth_vel_y += a_y * settings.d_t
    
    # Update position using velocity (same as: d_y = d_v_y * d_t; player.y += d_y)
    earth_x += earth_vel_x * settings.d_t
    earth_y += earth_vel_y * settings.d_t

    # Draw everything
    screen.fill(settings.black)  # Black space background
    
    # Draw sun (just a simple circle, no object)
    pygame.draw.circle(screen, settings.yellow, (sun_x, sun_y), sun_radius)
    
    # Draw earth (just a simple circle, no object)
    pygame.draw.circle(screen, settings.blue, (int(earth_x), int(earth_y)), earth_radius)

    pygame.display.flip()
    clock.tick(int(1/settings.d_t))

pygame.quit()
