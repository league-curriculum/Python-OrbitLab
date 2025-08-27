"""
uid: dN5vxWkG
name: Stage1

"""

import logging
import math
from dataclasses import dataclass

import pygame
from orbitlib.data import build_planet_data
from orbitlib.colors import Colors

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

pd = build_planet_data()

@dataclass
class Settings:

    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 1000

    SCREEN_CENTER: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    BACKGROUND_COLOR = Colors.BACKGROUND


    # Force and velocity vectors. 
    FORCE_COLOR = Colors.RED
    VELOCITY_COLOR = Colors.GREEN

    G: float = 6.67430e-11  # Gravitational constant (scaled for visualization)

    AU = 1.49597871e+11 # Astronomical Unit in km
    DIST_SCALE = AU / (SCREEN_WIDTH / 16) # Kilometers per pixel

    FPS: int = 60 # Frames per second draw update frames/wsec

    # Simulated secs per real sec ( ssec / wsec )
    #  (365 * 24 * 60 * 60) / 30  would be 30 seconds per year
    SIM_SEC_PER_SEC: float = (365 * 24 * 60 * 60) / 10

    #D_T: int = 60*30 # ssec/update
    #UPDATES_PER_FRAME: int = int(SIM_SEC_PER_SEC / (D_T * FPS))

    UPDATES_PER_FRAME: int = 3
    D_T: float = SIM_SEC_PER_SEC / (FPS * UPDATES_PER_FRAME)

    @classmethod
    def m2p(cls, meters: float|pygame.Vector2) -> float|pygame.Vector2:
        """Convert meters to pixels."""
        return meters / cls.DIST_SCALE

    @classmethod
    def p2m(cls, pixels: float|pygame.Vector2) -> float|pygame.Vector2:
        """Convert pixels to meters."""
        return pixels * cls.DIST_SCALE


class CelestialBody:
    """Base class for all celestial bodies."""
    def __init__(self, 
                 name: str,
                 position: tuple | pygame.Vector2, 
                 velocity: tuple | pygame.Vector2, 
                 color: tuple, radius: int, mass: int, settings: Settings):
        
        self.name = name
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
        logger.info(f"  Distance^2 from {self.name} to {other.name}: {r2}")

        if r2 == 0:
            return pygame.Vector2(0, 0)
       
        # Gravitational force magnitude

        logger.info(f"  masses: {self.mass * other.mass}")

        f_g = (self.settings.G * self.mass * other.mass) / r2
        logger.info(f"  Force due to {other.name}: {f_g}")

        # Force vector pointing towards the other body
        return (other.pos - self.pos).normalize() * f_g

    def update_physics(self, others: list["CelestialBody"]):
        """Advance the planet's state by one time step."""
        

        logger.info(f"Update {self.name} at pos {self.pos} vel {self.vel}")
        # Force from the sun
        self._force = pygame.Vector2(0,0)

        for other in others:
            if other is not self:
                f = self.force_due_to(other)
                
                self._force += f

        logger.info(f"Total force on {self.name}: {self._force}")

        # Acceleration of the planet, from f=ma
        a = self._force / self.mass
        
        # Integrate motion
        self.vel += a * self.settings.D_T         # v = a * t + v0
        self.pos += self.vel * self.settings.D_T  # x = v * t + x0

        logger.info(f"New position {self.name} at {self.pos} v={self.vel} a={a} f={self._force}")

    def draw(self, screen: pygame.Surface):
        """Draw the celestial body."""
        logger.info(f"Draw {self.name} at: {self.pos} {Settings.m2p(self.pos)}")
        pygame.draw.circle(screen, self.color, Settings.m2p(self.pos)+Settings.SCREEN_CENTER, self.radius)

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
    def __init__(self, name: str, position: tuple | pygame.Vector2, color: tuple, radius: int, mass: int, settings: Settings):
        super().__init__(name, position, (0,0), color, radius, mass, settings)


class Planet(CelestialBody):
    def __init__(self, name: str, position: tuple | pygame.Vector2, 
                 velocity: tuple | pygame.Vector2, 
                 color: tuple, radius: int, mass: int, settings: Settings):
        """Initialize a planet orbiting a star with position and velocity relative to the star."""
 
        super().__init__(name, position, velocity,  color, radius, mass, settings)


    def draw(self, screen: pygame.Surface):
        """Draw the planet and its vectors."""

        super().draw(screen)

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

    def __init__(self, bodies: list[CelestialBody] = None):
        # Initialize Pygame
        pygame.init()
        # Settings
        self.settings = Settings()


        # Screen and clock

        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))

        pygame.display.set_caption("Solar System")
        self.clock = pygame.time.Clock()

        self.bodies = bodies if bodies is not None else []
        self.running = False

    def add_bodies(self, bodies: list[CelestialBody]):
        """Add bodies to the simulation."""
        self.bodies.extend(bodies)

    def add_body(self, body: CelestialBody):
        """Add a single body to the simulation."""
        self.bodies.append(body)

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

        
    def run(self):
        """Main simulation loop with decoupled physics and rendering."""
        from itertools import count


        for i in count():
            t = Settings.D_T* i

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 
                
            for i in range(Settings.UPDATES_PER_FRAME):
                self.update()

            self.draw()

            self.clock.tick(self.settings.FPS)

    def dump(self):
        """Use tabulate to return a string table of: planet name, mass, xy position in km, xy position in pixels
        """
        import tabulate
        return tabulate.tabulate([[body.name, body.mass, body.pos, Settings.m2p(body.pos)] for body in self.bodies],
                        headers=["Name", "Mass (kg)", "Position (km)", "Position (pixels)"])


def main():
    """Main function to start the simulation."""

    settings = Settings()

    # Bodies
    sun = Star(
        "Sun",
        (0,0),
        Colors.LIGHT_YELLOW,
        15,
        pd['sun'].mass,
        settings
    )

    p0 = Planet(
        "Mercury",
        pd['mercury'].pos2,
        pd['mercury'].vel2,
        Colors.LIGHT_GRAY,
        3,
        pd['mercury'].mass,
        settings
    )

    p1 = Planet(
        "Venus",
        pd['venus'].pos2,
        pd['venus'].vel2,
        Colors.DARK_YELLOW,
        6,
        pd['venus'].mass,
        settings
    )

    p2 = Planet(
        "Earth",
        pd['earth'].pos2,
        pd['earth'].vel2,
        Colors.BLUE,
        8,
        pd['earth'].mass,
        settings
    )

    p3 = Planet(
        "Mars",
        pd['mars'].pos2,
        pd['mars'].vel2,
        Colors.RED,
        5,
        pd['mars'].mass,
        settings
    )

    p4 = Planet(
        "Jupiter",
        pd['jupiter'].pos2,
        pd['jupiter'].vel2,
        Colors.ORANGE,
        12,
        pd['jupiter'].mass,
        settings
    )

    bodies = [sun, p0, p1, p2, p3, p4]

    print("Scale:", Settings.m2p(Settings.AU))
    print("Simulated seconds per real second:", Settings.SIM_SEC_PER_SEC)
    print("Updates per frame:", Settings.UPDATES_PER_FRAME)
    print("Delta time (seconds):", Settings.D_T)

    s = Simulation(bodies)
    print(s.dump())

    s.run()


if __name__ == "__main__":
    main()