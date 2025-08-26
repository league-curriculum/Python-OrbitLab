"""
uid: dN5vxWkG
name: Stage1
"""

import pygame
import math
from dataclasses import dataclass
from skyfield.api import load


planets = load('de421.bsp')  # JPL ephemeris file

@dataclass
class Settings:

    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600

    SCREEN_CENTER: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    FPS: int = 60

    G: float = 0.5  # Gravitational constant (scaled for visualization)

    BACKGROUND_COLOR = (0, 0, 0)
    STAR_COLOR = (255, 255, 0)
    PLANET_1_COLOR = (0, 0, 255)
    PLANET_2_COLOR = (0, 255, 0)
    PLANET_3_COLOR = (255, 0, 0)
    PLANET_4_COLOR = (0, 255, 255)

    # Force and velocity vectors. 
    FORCE_COLOR = (255, 0, 0)
    VELOCITY_COLOR = (0, 255, 0)

    # Adjust the time scale to change the speed
    TIME_SCALE : int = 10

    AU = 1.49597871e+11 # Astronomical Unit in meters

    DIST_SCALE = AU / (SCREEN_WIDTH/2) # Meters per pixel

    def __post_init__(self):
        self.d_t = self.TIME_SCALE / self.FPS

    @classmethod
    def m2p(cls, meters: float|pygame.Vector2) -> float|pygame.Vector2:
        """Convert meters to pixels."""
        return meters * cls.DIST_SCALE

    @classmethod
    def p2m(cls, pixels: float|pygame.Vector2) -> float|pygame.Vector2:
        """Convert pixels to meters."""
        return pixels / cls.DIST_SCALE


class CelestialBody:
    """Base class for all celestial bodies."""
    def __init__(self, 
                 position: tuple | pygame.Vector2, 
                 velocity: tuple | pygame.Vector2, 
                 color: tuple, radius: int, mass: int, settings: Settings):
        
        self.color = color
        self.radius = radius
        self.mass = mass
        self.settings = settings

        self.pos = pygame.Vector2(position)
        self.vel = pygame.Vector2(velocity) 

    def force_due_to(self, other: "CelestialBody") -> pygame.Vector2:
        """Calculate the gravitational force exerted by another body on this planet."""
        # Distance squared between the two bodies

        r2 = self.pos.distance_squared_to(other.pos)
       
        if r2 == 0:
            return pygame.Vector2(0, 0)
       
        # Gravitational force magnitude
       
        f_g = (self.settings.G * self.mass * other.mass) / r2
       
        # Force vector pointing towards the other body
        return (other.pos - self.pos).normalize() * f_g

    def update_physics(self, others: list["CelestialBody"]):
        """Advance the planet's state by one time step."""
        
        # Force from the sun
        self._force = pygame.Vector2(0,0)

        for other in others:
            if other is not self:
                self._force += self.force_due_to(other)

        # Acceleration of the planet, from f=ma
        a = self._force / self.mass
        
        # Integrate motion
        self.vel += a * self.settings.d_t         # v = a * t + v0
        self.pos += self.vel * self.settings.d_t  # x = v * t + x0

    def update(self, others: list["CelestialBody"]):
        """Stars are static in this stage; nothing to update."""
        self.update_physics(others)


    def circ_orbit_vel(self, other: "CelestialBody"):
        """Calculate the circular orbital velocity needed to maintain a stable orbit."""
        r = self.pos.distance_to(other.pos)

        v =  math.sqrt(self.settings.G * other.mass / r)

        # Create a vector from sun to this body
        r_vec = self.pos - other.pos

        # Perpendicular direction (rotate 90 degrees counterclockwise)
        perp = r_vec.normalize().rotate(90)

        # Return velocity vector of magnitude v in perpendicular direction
        return perp * v

      

class Star(CelestialBody):
    def __init__(self, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int, settings: Settings):
        super().__init__(position, (0,0), color, radius, mass, settings)

    def draw(self, screen: pygame.Surface):
        """Draw the star."""
        pygame.draw.circle(screen, self.color, Settings.m2p(self.pos)+Settings.SCREEN_CENTER, self.radius)

class Planet(CelestialBody):
    def __init__(self, position: tuple | pygame.Vector2, 
                 velocity: tuple | pygame.Vector2, 
                 color: tuple, radius: int, mass: int, settings: Settings):
        """Initialize a planet orbiting a star with position and velocity relative to the star."""
 
        super().__init__(position, velocity,  color, radius, mass, settings)


    def draw(self, screen: pygame.Surface):
        """Draw the planet and its vectors."""

        pygame.draw.circle(screen, self.color, Settings.m2p(self.pos)+Settings.SCREEN_CENTER, self.radius)

        # Draw vectors (uses last computed force)
        #self.draw_vectors(screen, getattr(self, "_force", pygame.Vector2(0, 0)))

    def draw_vectors(self, screen: pygame.Surface, force: pygame.Vector2, scale: float = 20.0):
        """Draw the force and velocity vectors for the planet."""
        # Force vector (towards the sun)
        pygame.draw.line(screen, self.settings.FORCE_COLOR, Settings.m2p(self.pos), Settings.m2p(self.pos + force * scale), 2)
        # Velocity vector (direction of motion)
        pygame.draw.line(screen, self.settings.VELOCITY_COLOR, Settings.m2p(self.pos), Settings.m2p(self.pos + self.vel * scale), 2)


class Simulation:
    """Handle the main loop, updating and drawing bodies."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Settings
        self.settings = Settings()
        # Screen and clock
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Solar System")
        self.clock = pygame.time.Clock()


    def update(self):
        """Update physics for all bodies."""
        for body in self.bodies:
            body.update([other for other in self.bodies if other is not body])

    def draw(self):
        """Draw all bodies to the screen."""
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        for body in self.bodies:
            body.draw(self.screen)

        pygame.display.flip()

    def run(self, bodies: list[CelestialBody]):
        """Main simulation loop."""
        self.bodies = bodies 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw()
            self.clock.tick(self.settings.FPS)
        pygame.quit()


def main():
    """Main function to start the simulation."""

    settings = Settings()

    # Bodies
    sun = Star(
        (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
        settings.STAR_COLOR,
        10,
        100000,
        settings,
    )

    center = pygame.Vector2(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)

    p1 = Planet(
        center + pygame.Vector2(0, -100),
        (0, 0),
        settings.PLANET_1_COLOR,
        10,
        10,
        settings
    )

    p2 = Planet(
        center + pygame.Vector2(0, 100),
        (0, 0),
        settings.PLANET_2_COLOR,
        10,
        10,
        settings
    )

    # Set initial velocities for circular orbits around each other. 
    if False:
        p1.vel = p1.circ_orbit_vel(p2)/math.sqrt(2)
        p2.vel = p2.circ_orbit_vel(p1)/math.sqrt(2)

    p1.vel = p1.circ_orbit_vel(sun)
    p2.vel = p2.circ_orbit_vel(sun)

    bodies = [sun, p1, p2]

    Simulation().run(bodies)


if __name__ == "__main__":
    main()