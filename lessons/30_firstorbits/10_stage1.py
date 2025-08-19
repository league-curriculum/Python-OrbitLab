import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
d_T = 1 # timestep (delta time)
G = .5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System")

GREEN = (0, 255, 0)
RED = (255, 0, 0)

class CelestialBody:
    def __init__(self, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int):
        self.color = color
        self.radius = radius
        self.mass = mass
        # Convert position to Vector2 if it's a tuple
        if isinstance(position, tuple):
            self.pos = pygame.Vector2(position[0], position[1])
        else:
            self.pos = pygame.Vector2(position)

class Star(CelestialBody):
    def __init__(self, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int):
        super().__init__(position, color, radius, mass)
        
    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class Planet(CelestialBody):
    def __init__(self, sun: Star, position: tuple | pygame.Vector2, velocity: tuple | pygame.Vector2, color: tuple, radius: int, mass: int):
        
        """Initialize a planet with its orbiting star, position, velocity, color, radius, and mass.
        
        Args:
            sun (Star): The star this planet orbits.
            position (tuple | pygame.Vector2): The initial position of the planet, relative to the sun
            velocity (tuple | pygame.Vector2): The initial velocity of the planet.
            color (tuple): The color of the planet.
            radius (int): The radius of the planet.
            mass (int): The mass of the planet.

        """

        self.sun = sun  # Reference to the star this planet orbits

        super().__init__(position + self.sun.pos, color, radius, mass)

        # Convert velocity to Vector2 if it's a tuple
        
        self.vel = pygame.Vector2(*velocity) if isinstance(velocity, tuple) else velocity


    def force_vec_due_to(self, other: CelestialBody) -> pygame.Vector2:
        """Calculate the gravitational force exerted by another celestial body on this planet."""
        
        # Distance squared between the two bodies
        r2 = self.pos.distance_squared_to(other.pos)

        # Gravitational force magnitude
        f_g = (G * self.mass * other.mass) / r2 if r2 != 0 else 0

        # Force vector pointing towards the other body
        f = (other.pos - self.pos).normalize() * f_g

        return f

    def update(self):
        
        f = self.force_vec_due_to(self.sun)

        # Acceleration of the planet
        a = f / self.mass
       
        self.vel += a * d_T
        self.pos += self.vel * d_T

        print(self.pos, self.sun.pos, f)

        pygame.draw.circle(screen, self.color,self.pos, self.radius)

        pygame.draw.line(screen, RED, self.pos, self.pos + f * 20, 2)   # Force vector
        pygame.draw.line(screen, GREEN, self.pos, self.pos + self.vel * 20, 2)  # Velocity vector


# Main loop
running = True

# things

sun = Star((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (255, 255, 0), 20, 1000)

# The planet's position is defined relative to the sun. 
earth = Planet(sun,  (0, -200), (-1, 0), (0,0,255), 10, 100)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    screen.fill((0,0,0))
    sun.update()
    earth.update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
