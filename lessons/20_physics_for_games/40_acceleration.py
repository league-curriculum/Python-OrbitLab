"""
Accelerating Square - Object Oriented Version

This demonstrates acceleration using a spring force that pulls the square
toward the center of the screen. The square oscillates back and forth around
the center position, showing how acceleration affects velocity over time.

uid: 3hb3eMvH
name: Acceleration
"""

import pygame
from dataclasses import dataclass


@dataclass
class Settings:
    """Class to hold all game settings and constants."""

    # Screen settings
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600

    # Square settings
    SQUARE_SIZE: int = 50
    SQUARE_COLOR: tuple[int, int, int] = (255, 0, 0)  # Red

    # Physics settings
    K: float = 3.0  # Spring constant, controls how strong the spring force is
    MASS: float = 2.0  # Mass of the square, used to calculate acceleration

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)  # Black
    FPS: int = 60

    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = 1 / self.FPS  # Time step for physics calculations


class Simulation:
    """Class to handle the main simulation loop and physics calculations."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create settings object
        self.settings = Settings()

        # Initialize the screen
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Accelerating Red Square")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Initialize square position and physics
        self.x_pos = 20.0
        self.y_pos = (self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE) // 2
        self.velocity = 0.0

    def update_physics(self):
        """Update the square's position using spring force acceleration."""
        # Calculate the spring force, which is the force that pulls the square back
        # to the center, as if it was attached to a spring

        # Calculate the center position (target position for the spring)
        center_x = (self.settings.SCREEN_WIDTH - self.settings.SQUARE_SIZE) // 2

        # Calculate the spring force, accounting for mass (F = -k*x)
        # Force divided by mass gives acceleration (F = ma → a = F/m)
        acceleration = (-self.settings.K * (self.x_pos - center_x)) / self.settings.MASS

        # Update the velocity with the acceleration. Notice that we change
        # the velocity by adding the acceleration, not setting it to the acceleration,
        # and we change it a bit each frame.
        self.velocity += acceleration * self.settings.d_t

        # Update the position with the velocity. Like with the velocity, we change
        # the position by adding the velocity, not setting it to the velocity, and
        # we change it a bit each frame.
        self.x_pos += self.velocity * self.settings.d_t

    def draw(self):
        """Draw the square on the screen."""
        # Fill the screen with black (clears previous frame)
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the red square
        pygame.draw.rect(
            self.screen,
            self.settings.SQUARE_COLOR,
            (
                self.x_pos,
                self.y_pos,
                self.settings.SQUARE_SIZE,
                self.settings.SQUARE_SIZE,
            ),
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