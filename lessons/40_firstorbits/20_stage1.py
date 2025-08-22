"""
uid: dN5vxWkG
name: Stage1
"""

import pygame
from dataclasses import dataclass

@dataclass
class Settings:
    """Hold all simulation constants."""

    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    G: float = 0.5  # Gravitational constant (scaled for visualization)
    BACKGROUND_COLOR = (0, 0, 0)
    STAR_COLOR = (255, 255, 0)
    FORCE_COLOR = (255, 0, 0)
    VELOCITY_COLOR = (0, 255, 0)

    def __post_init__(self):
        self.d_t = 1.0 / self.FPS


# Initialize Pygame and settings
pygame.init()
settings = Settings()

# Set up the display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

class CelestialBody:
    def __init__(self, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int, settings: Settings):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.settings = settings
        # Convert position to Vector2 if it's a tuple
        if isinstance(position, tuple):
            self.pos = pygame.Vector2(position[0], position[1])
        else:
            self.pos = pygame.Vector2(position)

class Star(CelestialBody):
    def __init__(self, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int, settings: Settings):
        super().__init__(position, color, radius, mass, settings)
        
    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class Planet(CelestialBody):
    def __init__(self, sun: Star, position: tuple | pygame.Vector2, velocity: tuple | pygame.Vector2, color: tuple, radius: int, mass: int, settings: Settings):
        """Initialize a planet orbiting a star with position and velocity relative to the star."""
        self.sun = sun  # Reference to the star this planet orbits

        # Starting position is relative to the star
        rel_pos = pygame.Vector2(position) if isinstance(position, tuple) else pygame.Vector2(position)
        start_pos = rel_pos + self.sun.pos
        super().__init__(start_pos, color, radius, mass, settings)

        # Convert velocity to Vector2 if it's a tuple
        self.vel = pygame.Vector2(*velocity) if isinstance(velocity, tuple) else velocity
        if not isinstance(self.vel, pygame.Vector2):
            self.vel = pygame.Vector2(self.vel)


    def force_vec_due_to(self, other: CelestialBody) -> pygame.Vector2:
        """Calculate the gravitational force exerted by another body on this planet."""
        # Distance squared between the two bodies
        r2 = self.pos.distance_squared_to(other.pos)
        if r2 == 0:
            return pygame.Vector2(0, 0)
        # Gravitational force magnitude
        f_g = (self.settings.G * self.mass * other.mass) / r2
        # Force vector pointing towards the other body
        return (other.pos - self.pos).normalize() * f_g

    def update(self):
        # Force from the sun
        f = self.force_vec_due_to(self.sun)
        # Acceleration of the planet
        a = f / self.mass
        # Integrate motion
        self.vel += a * self.settings.d_t
        self.pos += self.vel * self.settings.d_t
        # Draw planet and vectors
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.line(screen, self.settings.FORCE_COLOR, self.pos, self.pos + f * 20, 2)  # Force vector
        pygame.draw.line(screen, self.settings.VELOCITY_COLOR, self.pos, self.pos + self.vel * 20, 2)  # Velocity vector


# Main loop
running = True

# things

sun = Star((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), settings.STAR_COLOR, 20, 1000, settings)

# The planet's position is defined relative to the sun. 
earth = Planet(sun,  (0, -200), (-1, 0), (0,0,255), 10, 100, settings)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    screen.fill(settings.BACKGROUND_COLOR)
    sun.update()
    earth.update()
    pygame.display.flip()
    pygame.time.Clock().tick(settings.FPS)

# Quit Pygame
pygame.quit()