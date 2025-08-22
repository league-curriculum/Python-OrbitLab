"""
uid: vxOyxbKP
name: Stage3
"""

import pygame
import math
import rebound
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System - Rebound Integration")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Astronomical constants (in SI units)
AU = 1.496e11  # Astronomical Unit in meters
M_SUN = 1.989e30  # Solar mass in kg
M_EARTH = 5.972e24  # Earth mass in kg
M_MERCURY = 3.301e23  # Mercury mass in kg
M_VENUS = 4.867e24  # Venus mass in kg
M_MARS = 6.4171e23  # Mars mass in kg
M_JUPITER = 1.898e27  # Jupiter mass in kg
G_SI = 6.67430e-11  # Gravitational constant in SI units

# Scaling factors for visualization
SCALE = 50 / AU  # pixels per meter (200 pixels = 1 AU)
TIME_SCALE = 24 * 3600  # 1 frame = 1 day in seconds
ZOOM_FACTOR = 1.0  # Global zoom factor

MAX_DISTANCE = 7.0 * AU  # Maximum distance from the central star to keep objects

class CelestialBody:
    """Base class for all celestial bodies."""
    def __init__(self, mass: float, color: tuple, radius: int, name: str):
        self.mass = mass
        self.color = color
        self.radius = radius
        self.name = name
        self.trail = []  # List of (position, timestamp) tuples
        self.max_trail_time = 365 * 24 * 3600  / 2

    def add_trail_point(self, pos: tuple, timestamp: float):
        """Add a point to the trail with timestamp and manage trail length by time."""
        self.trail.append((pos, timestamp))
        
        # Remove old trail points based on time
        cutoff_time = timestamp - self.max_trail_time
        self.trail = [(p, t) for p, t in self.trail if t >= cutoff_time]
    
    def get_trail(self) -> list:
        """Get the current trail positions only."""
        return [pos for pos, timestamp in self.trail]

class Star(CelestialBody):
    """Represents a star (fixed at origin)."""
    def __init__(self, mass: float, color: tuple, radius: int, name: str):
        super().__init__(mass, color, radius, name)

class Planet(CelestialBody):
    """Represents a planet with orbital parameters."""
    def __init__(self, mass: float, color: tuple, radius: int, name: str, 
                 orbital_distance: float, orbital_velocity: float, 
                 eccentricity: float = 0.0, inclination: float = 0.0):
        
        super().__init__(mass, color, radius, name)
        self.orbital_distance = orbital_distance
        self.orbital_velocity = orbital_velocity
        self.eccentricity = eccentricity
        self.inclination = inclination
    
    def get_initial_velocity(self, central_mass: float) -> float:
        """Calculate initial velocity based on orbital parameters.
        
        Args:
            central_mass: Mass of the central body
            
        Returns:
            Initial velocity in m/s
        """
        if self.eccentricity == 0:
            # Circular orbit - use provided orbital velocity
            return self.orbital_velocity
        else:
            # Elliptical orbit - calculate velocity at aphelion
            return math.sqrt(G_SI * central_mass * (1 - self.eccentricity) / 
                           (self.orbital_distance * (1 + self.eccentricity)))
    
    def get_initial_state(self, central_mass: float) -> tuple:
        """Calculate initial position and velocity based on orbital parameters.
        
        Args:
            central_mass: Mass of the central body
            
        Returns:
            Tuple of (x, y, z, vx, vy, vz) in SI units
        """
        # Calculate position based on orbital distance and eccentricity
        if self.eccentricity == 0:
            # Circular orbit
            x = self.orbital_distance
            y = 0
            vx = 0
            vy = self.get_initial_velocity(central_mass)
        else:
            # Elliptical orbit - start at aphelion for highly eccentric orbits
            x = self.orbital_distance * (1 + self.eccentricity)
            y = 0
            vx = 0
            vy = self.get_initial_velocity(central_mass)
        
        # Rotate the x, y position around the central body, randomly
        angle = np.random.uniform(0, 2 * math.pi)
        pos = pygame.Vector2(x, y)
        rotated_pos = pos.rotate_rad(angle)
        x, y = rotated_pos.x, rotated_pos.y

        # Also rotate the velocity vector
        vel = pygame.Vector2(vx, vy)
        rotated_vel = vel.rotate_rad(angle)
        vx, vy = rotated_vel.x, rotated_vel.y


        # Add inclination if specified
        if self.inclination != 0:
            z = y * math.sin(self.inclination)
            y = y * math.cos(self.inclination)
            vz = vy * math.sin(self.inclination)
            vy = vy * math.cos(self.inclination)
        else:
            z = 0
            vz = 0
        
        return (x, y, z, vx, vy, vz)

class Asteroid(Planet):
    """Represents an asteroid - similar to Planet but not displayed in name list."""
    def __init__(self, mass: float, color: tuple, radius: int, name: str, 
                 orbital_distance: float, orbital_velocity: float, 
                 eccentricity: float = 0.0, inclination: float = 0.0):
        super().__init__(mass, color, radius, name, orbital_distance, orbital_velocity, eccentricity, inclination)



class SolarSystemSimulation:
    def __init__(self, bodies: list[CelestialBody]):
        """Initialize the solar system simulation with provided celestial bodies.
        
        Args:
            bodies: List of CelestialBody objects (first body becomes the fixed origin)
        """
        if not bodies:
            raise ValueError("At least one celestial body must be provided")
        
        self.bodies = bodies
        self.central_body = bodies[0]  # First body is the fixed origin
        
        # Create Rebound simulation
        self.sim = rebound.Simulation()
        self.sim.G = G_SI
        self.sim.units = ('m', 'kg', 's')
        
        # Add the central body at origin
        self.sim.add(m=self.central_body.mass, x=0, y=0, z=0, vx=0, vy=0, vz=0)
        
        # Add remaining bodies with their orbital parameters (skip the first body)
        for body in self.bodies[1:]:
            # Only planets have orbital parameters
            if isinstance(body, Planet):
                x, y, z, vx, vy, vz = body.get_initial_state(self.central_body.mass)

                self.sim.add(m=body.mass, x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)
            else:
                # For non-Planet celestial bodies, add at origin with zero velocity
                self.sim.add(m=body.mass, x=0, y=0, z=0, vx=0, vy=0, vz=0)
        
        # Move to center-of-mass frame
        self.sim.move_to_com()
        
        # Set up integration
        self.sim.integrator = "whfast"
        self.sim.dt = TIME_SCALE
        
        # Create body properties list for visualization
        self.body_props = []
        
        # Add properties for all bodies
        for body in self.bodies:
            self.body_props.append({
                "color": body.color,
                "radius": body.radius,
                "name": body.name
            })
        
    def screen_pos(self, x, y):
        """Convert simulation coordinates to screen coordinates"""
        screen_x = int(x * SCALE * ZOOM_FACTOR + SCREEN_WIDTH // 2)
        screen_y = int(-y * SCALE * ZOOM_FACTOR + SCREEN_HEIGHT // 2)  # Flip Y axis
        return (screen_x, screen_y)
    
    def update_simulation(self):
        """Advance the simulation by one time step"""
        self.sim.integrate(self.sim.t + self.sim.dt)
        
        # Remove objects that are more than 5 AU from the star
        self.remove_distant_objects()
        
        # Update trails with current simulation time
        for i, particle in enumerate(self.sim.particles):
            pos = self.screen_pos(particle.x, particle.y)
            if i < len(self.bodies):
                self.bodies[i].add_trail_point(pos, self.sim.t)
    
    def remove_distant_objects(self):
        """Remove objects that are more than 5 AU from the central star"""
        
        
        # Check particles in reverse order to avoid index issues when removing
        for i in range(len(self.sim.particles) - 1, 0, -1):  # Skip index 0 (central star)
            particle = self.sim.particles[i]
            distance = math.sqrt(particle.x**2 + particle.y**2 + particle.z**2)
            
            if distance > MAX_DISTANCE:
                # Remove from simulation
                self.sim.remove(i)
                
                # Remove corresponding entries from our tracking lists
                if i < len(self.bodies):
                    self.bodies.pop(i)
                if i < len(self.body_props):
                    self.body_props.pop(i)

    
    def draw(self, screen):
        """Draw the simulation on the screen"""
        # Clear screen
        screen.fill(BLACK)
        
        # Draw trails
        for i, body in enumerate(self.bodies):
            if i < len(self.sim.particles):
                trail = body.get_trail()
                if len(trail) > 1:
                    # Draw trail with fading effect
                    for j in range(1, len(trail)):
                        alpha = j / len(trail)
                        color = tuple(int(c * alpha) for c in body.color)
                        if j < len(trail) - 1:
                            pygame.draw.line(screen, color, trail[j-1], trail[j], 1)
        
        # Draw bodies
        for i, particle in enumerate(self.sim.particles):
            pos = self.screen_pos(particle.x, particle.y)
            
            # Only draw if on screen
            if 0 <= pos[0] <= SCREEN_WIDTH and 0 <= pos[1] <= SCREEN_HEIGHT:
                pygame.draw.circle(screen, self.body_props[i]["color"], pos, self.body_props[i]["radius"])
                
                # Draw velocity vector (scaled for visibility)
                vel_scale = 1e-4  # Scale factor for velocity vectors
                vel_end = (
                    int(pos[0] + particle.vx * vel_scale),
                    int(pos[1] - particle.vy * vel_scale)  # Flip Y axis
                )
                pygame.draw.line(screen, GREEN, pos, vel_end, 2)
                
                # Draw name only if not an asteroid
                if not isinstance(self.bodies[i], Asteroid):
                    font = pygame.font.Font(None, 24)
                    text = font.render(self.body_props[i]["name"], True, WHITE)
                    text_rect = text.get_rect(center=(pos[0], pos[1] - self.body_props[i]["radius"] - 15))
                    screen.blit(text, text_rect)
        
        # Draw simulation info
        self.draw_info(screen)
    
    def draw_info(self, screen):
        """Draw simulation information on screen"""
        font = pygame.font.Font(None, 24)
        
        info_lines = [f"Time: {self.sim.t / (24 * 3600):.1f} days"]
        
        # Show information for each orbiting body
        for i, body in enumerate(self.bodies[1:]):  # Skip the central body
            particle_index = i + 1  # Skip the central body (index 0)
            if isinstance(body, Asteroid):
                continue
            if particle_index < len(self.sim.particles):
                particle = self.sim.particles[particle_index]
                distance = math.sqrt(particle.x**2 + particle.y**2)
                speed = math.sqrt(particle.vx**2 + particle.vy**2)
                
                info_lines.append(f"{body.name}: {distance / AU:.3f} AU, {speed / 1000:.1f} km/s")
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, 10 + i * 25))

# Create celestial bodies for demonstration
def create_demo_system():
    """Create a demonstration system with Mercury, Venus, Earth, and an asteroid."""
    
    # Create the Sun
    sun = Star(mass=M_SUN, color=YELLOW, radius=10, name="Sun")
    
    # Create planets with realistic orbital parameters
    mercury = Planet(
        mass=M_MERCURY, 
        color=GRAY, 
        radius=4, 
        name="Mercury",
        orbital_distance=0.387 * AU,  # 0.387 AU from Sun
        orbital_velocity=math.sqrt(G_SI * M_SUN / (0.387 * AU)),  # Circular velocity
        eccentricity=0.0  # Simplified to circular for clarity
    )
    
    venus = Planet(
        mass=M_VENUS, 
        color=ORANGE, 
        radius=6, 
        name="Venus",
        orbital_distance=0.723 * AU,  # 0.723 AU from Sun
        orbital_velocity=math.sqrt(G_SI * M_SUN / (0.723 * AU)),
        eccentricity=0.0
    )
    
    mars = Planet(  
        mass=M_MARS, 
        color=(255, 0, 0),  # Red color for Mars
        radius=5, 
        name="Mars",
        orbital_distance=1.524 * AU,  # 1.524 AU from Sun
        orbital_velocity=math.sqrt(G_SI * M_SUN / (1.524 * AU)),
        eccentricity=0.0934  # Mars' eccentricity
    )   

    earth = Planet(
        mass=M_EARTH * 10_000, 
        color=BLUE, 
        radius=8, 
        name="Earth",
        orbital_distance=1.0 * AU,  # 1 AU from Sun
        orbital_velocity=math.sqrt(G_SI * M_SUN / AU),
        eccentricity=0.0
    )


    
    jupiter = Planet(
        mass=M_JUPITER,  # Jupiter mass in kg
        color=(255, 165, 0),  # Orange color for Jupiter
        radius=12,  # Visual size
        name="Jupiter",
        orbital_distance=5.2 * AU,  # 5.2 AU from Sun
        orbital_velocity=math.sqrt(G_SI * M_SUN / (5.2 * AU)),
        eccentricity=0.0489  # Jupiter's eccentricity
    )


    asteroids = []
    for i in range(1000):
        # Random orbital properties
        distance = np.random.uniform(.7, 7.0) * AU  # Between 1.1 and 7.0 AU (asteroid belt)
        ecc =np.random.uniform(0.0, 0.9)  
        inclination = 0 # np.random.uniform(0.0, 0.3)  # Inclination up to 0.3 radians (~17 degrees)
        
        # Random physical properties
        size = 2 # np.random.uniform(1, 4)  # Visual si`ze between 1-3 pixels
        mass = np.random.uniform(1e8, 1e17)  # Mass between 10^9 and 10^17 kg

        # Random color variation (shades of gray to white)
        gray_shade = np.random.randint(150, 255)
        color = (gray_shade, gray_shade, gray_shade)
        
        # Create the asteroid
        new_asteroid = Asteroid(
            mass=mass,
            color=color,
            radius=int(size),
            name=f"Asteroid {i+1}",
            orbital_distance=distance,
            orbital_velocity=math.sqrt(G_SI * M_SUN / distance),
            eccentricity=ecc,
            inclination=inclination
        )
        
        asteroids.append(new_asteroid)



    return [sun, mercury, venus, earth, mars, jupiter, *asteroids]

# Create the demonstration system
bodies = create_demo_system()
simulation = SolarSystemSimulation(bodies)

# Main loop
running = True
clock = pygame.time.Clock()
paused = False
time_multiplier = 1.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reset simulation
                bodies = create_demo_system()
                simulation = SolarSystemSimulation(bodies)
            elif event.key == pygame.K_p:
                # Pause/unpause
                paused = not paused
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                # Speed up time
                time_multiplier *= 2
                simulation.sim.dt = TIME_SCALE * time_multiplier
            elif event.key == pygame.K_MINUS:
                # Slow down time
                time_multiplier /= 2
                simulation.sim.dt = TIME_SCALE * time_multiplier
            elif event.key == pygame.K_z:
                # Zoom in
                ZOOM_FACTOR *= 1.2
            elif event.key == pygame.K_x:
                # Zoom out
                ZOOM_FACTOR /= 1.2
    
    # Update and draw
    if not paused:
        simulation.update_simulation()
    simulation.draw(screen)
    
    # Draw controls info
    font = pygame.font.Font(None, 20)
    controls = [
        "Controls:",
        "SPACE - Reset",
        "P - Pause/Unpause",
        "+/- - Speed up/slow time",
        "Z/X - Zoom in/out"
    ]
    
    for i, control in enumerate(controls):
        text = font.render(control, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 20))
    
    # Show time multiplier and zoom
    status_text = font.render(f"Time: {time_multiplier:.1f}x, Zoom: {ZOOM_FACTOR:.1f}x", True, WHITE)
    screen.blit(status_text, (SCREEN_WIDTH - 200, 120))
    
    if paused:
        pause_text = font.render("PAUSED", True, RED)
        screen.blit(pause_text, (SCREEN_WIDTH - 200, 140))
    
    pygame.display.flip()
    clock.tick(200)  # 60 FPS

# Quit Pygame
pygame.quit()