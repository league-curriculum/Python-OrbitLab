"""
Accelerating Square with Body Class - Advanced Object Oriented Version

This demonstrates acceleration using a spring force that pulls the square
toward the center of the screen. The square oscillates back and forth around
the center position, showing how acceleration affects velocity over time.

This version introduces a Body class that encapsulates the physics properties
(position, velocity, acceleration) and behavior (update, draw) of the moving object.
This separation of concerns makes the code more modular and easier to extend.

uid: 2C6XBKVG
name: Acceleration Body
"""

import pygame
from dataclasses import dataclass
from orbitlib.colors import Colors


@dataclass
class Settings:
    """Class to hold all game settings and constants."""

    # Screen settings
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600

    # Square settings
    SQUARE_SIZE: int = 50
    SQUARE_COLOR: tuple[int, int, int] = Colors.RED

    # Physics settings
    K: float = 3.0  # Spring constant, controls how strong the spring force is
    MASS: float = 2.0  # Mass of the square, used to calculate acceleration

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = Colors.BLACK
    FPS: int = 60

    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = 1 / self.FPS  # Time step for physics calculations


class Body:
    """Class representing a physical body with position, velocity, and acceleration."""

    def __init__(
        self,
        x: float,
        y: float,
        mass: float,
        settings: Settings,
        v_x: float = 0.0,
        v_y: float = 0.0,
    ):
        """Initialize the body with position, physics properties, and optional initial velocity."""
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = 0.0
        self.a_y = 0.0
        self.mass = mass
        self.settings = settings

    def apply_spring_force(self, t_x: float, t_y: float, k: float):
        """Apply spring force toward a target position."""
        # Calculate displacement from target
        d_x = self.x - t_x
        d_y = self.y - t_y

        # Calculate spring force (F = -k * displacement)
        f_x = -k * d_x
        f_y = -k * d_y

        # Calculate acceleration (F = ma → a = F/m)
        self.a_x = f_x / self.mass
        self.a_y = f_y / self.mass

    def update(self):
        """Update the body's position and velocity based on acceleration."""
        # Update velocity with acceleration
        self.v_x += self.a_x * self.settings.d_t
        self.v_y += self.a_y * self.settings.d_t

        # Update position with velocity
        self.x += self.v_x * self.settings.d_t
        self.y += self.v_y * self.settings.d_t

        # Reset acceleration (forces need to be applied each frame)
        self.a_x = 0.0
        self.a_y = 0.0

    def draw(self, screen: pygame.Surface):
        """Draw the body on the screen."""
        pygame.draw.rect(
            screen,
            self.settings.SQUARE_COLOR,
            (self.x, self.y, self.settings.SQUARE_SIZE, self.settings.SQUARE_SIZE),
        )


class Simulation:
    """Class to handle the main simulation loop and coordinate the physics simulation."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create settings object
        self.settings = Settings()

        # Initialize the screen
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Accelerating Square with Body Class")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Create the body object
        start_x = 0
        start_y = (self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE) // 2

        self.body = Body(start_x, start_y, self.settings.MASS, self.settings)

        # Calculate the target position (center of screen)
        self.t_x = (self.settings.SCREEN_WIDTH - self.settings.SQUARE_SIZE) // 2
        self.t_y = (self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE) // 2

    def update_physics(self):
        """Update the physics simulation."""
        # Apply spring force toward the center
        self.body.apply_spring_force(self.t_x, self.t_y, self.settings.K)

        # Update the body's physics
        self.body.update()

    def draw(self):
        """Draw everything on the screen."""
        # Clear the screen
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the body
        self.body.draw(self.screen)

        # Optionally draw the target position as a small circle
        pygame.draw.circle(
            self.screen,
            Colors.GREEN,  # Green color for target
            (
                int(self.t_x + self.settings.SQUARE_SIZE // 2),
                int(self.t_y + self.settings.SQUARE_SIZE // 2),
            ),
            5,
        )

        # Update the display
        pygame.display.flip()

    def run(self):
        """Main simulation loop."""
        running = True

        while running:
            # Event handling
            for event in pygame.event.get():
                # Check for clicking the close button
                if event.type == pygame.QUIT:
                    running = False

            # Update physics
            self.update_physics()

            # Draw everything
            self.draw()

            # Frame rate control
            self.clock.tick(self.settings.FPS)

        # Quit Pygame
        pygame.quit()


def main():
    """Main function to start the simulation."""
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()
