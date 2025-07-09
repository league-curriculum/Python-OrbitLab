import pygame
import math
import rebound
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System - Rebound Integration (Extended)")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

# Astronomical constants (in SI units)
AU = 1.496e11  # Astronomical Unit in meters
M_SUN = 1.989e30  # Solar mass in kg
M_EARTH = 5.972e24  # Earth mass in kg
M_MOON = 7.342e22  # Moon mass in kg
G_SI = 6.67430e-11  # Gravitational constant in SI units

# Moon orbital parameters
MOON_DISTANCE = 3.844e8  # Average Earth-Moon distance in meters
MOON_ORBITAL_VELOCITY = 1022  # m/s

# Scaling factors for visualization
SCALE = 300 / AU  # pixels per meter (300 pixels = 1 AU)
TIME_SCALE = 24 * 3600  # 1 frame = 1 day in seconds

class SolarSystemSimulation:
    def __init__(self, include_moon=True):
        # Create Rebound simulation
        self.sim = rebound.Simulation()
        self.sim.G = G_SI
        self.sim.units = ('m', 'kg', 's')
        
        # Add Sun at origin
        self.sim.add(m=M_SUN, x=0, y=0, z=0, vx=0, vy=0, vz=0)
        
        # Add Earth with correct orbital parameters
        earth_orbital_velocity = math.sqrt(G_SI * M_SUN / AU)  # Circular orbital velocity
        self.sim.add(m=M_EARTH, x=AU, y=0, z=0, vx=0, vy=earth_orbital_velocity, vz=0)
        
        # Add Moon if requested
        if include_moon:
            # Moon orbits Earth, so we need to add its orbital velocity to Earth's
            moon_x = AU + MOON_DISTANCE
            moon_vy = earth_orbital_velocity + MOON_ORBITAL_VELOCITY
            self.sim.add(m=M_MOON, x=moon_x, y=0, z=0, vx=0, vy=moon_vy, vz=0)
        
        # Move to center-of-mass frame
        self.sim.move_to_com()
        
        # Set up integration
        self.sim.integrator = "whfast"
        self.sim.dt = TIME_SCALE
        
        # Visual properties for each body
        self.body_props = [
            {"color": YELLOW, "radius": 25, "name": "Sun"},
            {"color": BLUE, "radius": 10, "name": "Earth"}
        ]
        
        if include_moon:
            self.body_props.append({"color": GRAY, "radius": 5, "name": "Moon"})
        
        # For trail visualization
        self.trails = [[] for _ in range(len(self.body_props))]
        self.max_trail_length = 300
        
        # Zoom and pan controls
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Time control
        self.paused = False
        self.time_multiplier = 1.0
        
    def screen_pos(self, x, y):
        """Convert simulation coordinates to screen coordinates"""
        screen_x = int((x * SCALE * self.zoom) + SCREEN_WIDTH // 2 + self.pan_x)
        screen_y = int((-y * SCALE * self.zoom) + SCREEN_HEIGHT // 2 + self.pan_y)  # Flip Y axis
        return (screen_x, screen_y)
    
    def update_simulation(self):
        """Advance the simulation by one time step"""
        if not self.paused:
            self.sim.integrate(self.sim.t + self.sim.dt * self.time_multiplier)
            
            # Update trails
            for i, particle in enumerate(self.sim.particles):
                pos = self.screen_pos(particle.x, particle.y)
                # Only add to trail if position is reasonable
                if abs(pos[0]) < 10000 and abs(pos[1]) < 10000:
                    self.trails[i].append(pos)
                    
                    # Limit trail length
                    if len(self.trails[i]) > self.max_trail_length:
                        self.trails[i].pop(0)
    
    def draw(self, screen):
        """Draw the simulation on the screen"""
        # Clear screen
        screen.fill(BLACK)
        
        # Draw trails
        for i, trail in enumerate(self.trails):
            if len(trail) > 1:
                # Draw trail with fading effect
                for j in range(1, len(trail)):
                    alpha = j / len(trail)
                    color = tuple(int(c * alpha) for c in self.body_props[i]["color"])
                    if j < len(trail) - 1:
                        pygame.draw.line(screen, color, trail[j-1], trail[j], 1)
        
        # Draw bodies
        for i, particle in enumerate(self.sim.particles):
            pos = self.screen_pos(particle.x, particle.y)
            
            # Only draw if reasonably close to screen
            if -500 <= pos[0] <= SCREEN_WIDTH + 500 and -500 <= pos[1] <= SCREEN_HEIGHT + 500:
                # Draw body
                pygame.draw.circle(screen, self.body_props[i]["color"], pos, 
                                 max(1, int(self.body_props[i]["radius"] * self.zoom)))
                
                # Draw velocity vector (scaled for visibility)
                vel_scale = 1e-4 * self.zoom  # Scale factor for velocity vectors
                vel_end = (
                    int(pos[0] + particle.vx * vel_scale),
                    int(pos[1] - particle.vy * vel_scale)  # Flip Y axis
                )
                pygame.draw.line(screen, GREEN, pos, vel_end, max(1, int(2 * self.zoom)))
                
                # Draw name
                if self.zoom > 0.5:  # Only show names when zoomed in enough
                    font = pygame.font.Font(None, max(16, int(24 * self.zoom)))
                    text = font.render(self.body_props[i]["name"], True, WHITE)
                    text_rect = text.get_rect(center=(pos[0], pos[1] - self.body_props[i]["radius"] * self.zoom - 15))
                    screen.blit(text, text_rect)
        
        # Draw simulation info
        self.draw_info(screen)
        
        # Draw controls
        self.draw_controls(screen)
    
    def draw_info(self, screen):
        """Draw simulation information on screen"""
        font = pygame.font.Font(None, 24)
        
        # Calculate Earth's orbital period in days
        earth = self.sim.particles[1]
        earth_distance = math.sqrt(earth.x**2 + earth.y**2)
        earth_speed = math.sqrt(earth.vx**2 + earth.vy**2)
        
        # Calculate Moon info if present
        info_lines = [
            f"Time: {self.sim.t / (24 * 3600):.1f} days ({self.sim.t / (365.25 * 24 * 3600):.3f} years)",
            f"Earth distance: {earth_distance / AU:.3f} AU",
            f"Earth speed: {earth_speed / 1000:.1f} km/s (expected: 29.8 km/s)",
            f"Zoom: {self.zoom:.2f}x",
            f"Time multiplier: {self.time_multiplier:.1f}x"
        ]
        
        if len(self.sim.particles) > 2:  # Moon is present
            moon = self.sim.particles[2]
            earth_moon_distance = math.sqrt((moon.x - earth.x)**2 + (moon.y - earth.y)**2)
            moon_speed = math.sqrt(moon.vx**2 + moon.vy**2)
            info_lines.append(f"Earth-Moon distance: {earth_moon_distance / 1000:.0f} km")
            info_lines.append(f"Moon speed: {moon_speed / 1000:.1f} km/s")
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, 10 + i * 25))
    
    def draw_controls(self, screen):
        """Draw control instructions"""
        font = pygame.font.Font(None, 20)
        controls = [
            "Controls:",
            "SPACE: Pause/Resume",
            "R: Reset simulation",
            "↑/↓: Zoom in/out",
            "WASD: Pan view",
            "+/-: Speed up/slow down time"
        ]
        
        for i, control in enumerate(controls):
            color = YELLOW if i == 0 else WHITE
            text = font.render(control, True, color)
            screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 22))
    
    def handle_input(self, keys):
        """Handle keyboard input for controls"""
        # Zoom controls
        if keys[pygame.K_UP]:
            self.zoom *= 1.02
        if keys[pygame.K_DOWN]:
            self.zoom /= 1.02
            
        # Pan controls
        pan_speed = 5
        if keys[pygame.K_w]:
            self.pan_y += pan_speed
        if keys[pygame.K_s]:
            self.pan_y -= pan_speed
        if keys[pygame.K_a]:
            self.pan_x += pan_speed
        if keys[pygame.K_d]:
            self.pan_x -= pan_speed
            
        # Time controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.time_multiplier = min(10.0, self.time_multiplier * 1.1)
        if keys[pygame.K_MINUS]:
            self.time_multiplier = max(0.1, self.time_multiplier / 1.1)

def main():
    # Create simulation instance
    simulation = SolarSystemSimulation(include_moon=True)
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation.paused = not simulation.paused
                elif event.key == pygame.K_r:
                    # Reset simulation
                    simulation = SolarSystemSimulation(include_moon=True)
        
        # Handle continuous input
        simulation.handle_input(keys)
        
        # Update and draw
        simulation.update_simulation()
        simulation.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
