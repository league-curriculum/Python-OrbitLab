"""
Moving Square - Object Oriented Version

All this game does is move a square around the screen using the arrow keys.
The square is constrained to the screen, so it can't go off the edges.

Move the square around the screen with the arrow keys. 

name: Moving Square
uid: BXW9x2OW
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
    SQUARE_COLOR: tuple[int, int, int] = (
        0,
        128,
        255,
    )  # Red-Green-Blue color in the range 0-255
    
    SQUARE_SPEED: int = 300  # Speed of the square in pixels per second

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = (255, 255, 255)  # White
    FPS: int = 60

    def __post_init__(self):
        """Calculate derived values after initialization."""
        # Physics settings
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
        pygame.display.set_caption("Move the Square")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Initialize square position
        self.x = self.settings.SCREEN_WIDTH // 2 - self.settings.SQUARE_SIZE // 2
        self.y = self.settings.SCREEN_HEIGHT // 2 - self.settings.SQUARE_SIZE // 2

    def handle_input(self):
        """Handle keyboard input and return velocity changes."""
        # Get the keys pressed. Gets an array of all the keys
        # with a boolean value of whether they are pressed or not
        keys = pygame.key.get_pressed()

        # Calculate the change in the position
        d_x = 0
        d_y = 0

        # Move the square based on arrow keys
        if keys[pygame.K_LEFT]:
            d_x = -self.settings.SQUARE_SPEED * self.settings.d_t

        if keys[pygame.K_RIGHT]:
            d_x = self.settings.SQUARE_SPEED * self.settings.d_t

        if keys[pygame.K_UP]:
            d_y = -self.settings.SQUARE_SPEED * self.settings.d_t

        if keys[pygame.K_DOWN]:
            d_y = self.settings.SQUARE_SPEED * self.settings.d_t

        return d_x, d_y

    def update_position(self, d_x, d_y):
        """Update the square's position and constrain it to the screen."""
        # Update the position of the square
        self.x = self.x + d_x
        self.y = self.y + d_y

        # Prevent the square from going off the screen
        self.x = max(
            0, min(self.settings.SCREEN_WIDTH - self.settings.SQUARE_SIZE, self.x)
        )
        self.y = max(
            0, min(self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE, self.y)
        )

    def draw(self):
        """Draw the square on the screen."""
        # This will clear the screen by filling it
        # with the background color. If we didn't do this,
        # the square would leave a trail behind it.
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the square
        pygame.draw.rect(
            self.screen,
            self.settings.SQUARE_COLOR,
            (self.x, self.y, self.settings.SQUARE_SIZE, self.settings.SQUARE_SIZE),
        )

        # Update the display. Imagine that the screen is two different whiteboards. One
        # whiteboard is currently visible to the player, and the other whiteboard is being
        # drawn on. When you call pygame.display.flip(), it's like taking the whiteboard
        # that was being drawn on and showing it to the player, while taking the whiteboard
        # that was visible to the player and giving it to the artist to draw on. This makes
        # it so that the player never sees the drawing process, only the final result.
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

            # Handle input and get movement
            d_x, d_y = self.handle_input()

            # Update position
            self.update_position(d_x, d_y)

            # Draw everything
            self.draw()

            # Cap the frame rate. This makes the game run at a consistent speed on all computers.
            self.clock.tick(self.settings.FPS)

        # Quit Pygame
        pygame.quit()


def main():
    """Main function to start the simulation."""
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()