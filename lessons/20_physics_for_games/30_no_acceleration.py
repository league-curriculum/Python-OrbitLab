"""
Move a square, with no acceleration - Object Oriented Version

This version uses Object Oriented Programming with a Settings dataclass to hold
all constants and a Simulation class to handle the main loop and game logic.
The square moves automatically left and right, bouncing off the screen edges.

uid: igVBJmhm
name: No Acceleration
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
    SQUARE_SPEED: int = 300

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)  # Black
    FPS: int = 60  # Frames per second

    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = 1 / self.FPS  # Time step for physics calculations


class Simulation:
    """Class to handle the main simulation loop and game logic."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create settings object
        self.settings = Settings()

        # Initialize the screen
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Moving Red Square")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Initialize square position
        self.x = 0
        self.y = (self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE) // 2

        # Movement direction: 1 for right, -1 for left
        self.direction = 1

    def update_position(self):
        """Update the square's position and handle bouncing off screen edges."""
        # Move the square, a bit each frame
        d_x = self.settings.SQUARE_SPEED * self.direction * self.settings.d_t
        self.x += d_x

        # Check for screen bounds and reverse direction if necessary
        if self.x + self.settings.SQUARE_SIZE > self.settings.SCREEN_WIDTH:
            self.direction = -1  # Move left
        elif self.x < 0:
            self.direction = 1  # Move right

    def draw(self):
        """Draw the square on the screen."""
        # Fill the screen with black (clears previous frame)
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the red square
        pygame.draw.rect(
            self.screen,
            self.settings.SQUARE_COLOR,
            (self.x, self.y, self.settings.SQUARE_SIZE, self.settings.SQUARE_SIZE),
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

            # Update position
            self.update_position()

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