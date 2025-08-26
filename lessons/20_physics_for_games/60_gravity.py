"""
Implementing Gravity 

This program demonstrates a simple implementation of gravity in a game,
with the player constantly jumping. Notice that using gravity makes the player
jump more realistic. The player goes up quickly, but falls slowly.

uid: 3IDQVkBh
name: Gravity
"""

import pygame
from dataclasses import dataclass


@dataclass
class Settings:
    """Class to hold all game settings and constants."""

    # Screen settings
    SCREEN_WIDTH: int = 500
    SCREEN_HEIGHT: int = 500

    # Player settings
    PLAYER_SIZE: int = 10
    PLAYER_COLOR: tuple[int, int, int] = (0, 0, 0)  # Black
    PLAYER_X: int = 100  # Initial x position of the player

    # Physics settings
    JUMP_VELOCITY: float = 200.0  # Initial upward velocity when jumping
    GRAVITY: float = 60.0  # Gravitational acceleration (downward)
    MASS: float = 2.0  # Mass of the player

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = (255, 255, 255)  # White
    FPS: int = 30
    TIMESCALE: int = 1

    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = self.TIMESCALE / self.FPS  # Time step for physics calculations


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
        self.size = settings.PLAYER_SIZE

    def apply_gravity(self, gravity: float):
        """Apply gravitational force (downward acceleration)."""
        self.a_y = gravity

    def jump(self, jump_velocity: float):
        """Initiate a jump by setting upward velocity."""
        self.v_y = -jump_velocity n# Negative because up is negative in screen coordinates

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

    def check_ground_collision(self, ground_y: float):
        """Check if the body hits the ground and handle collision."""
        if self.y + self.size >= ground_y:
            self.y = ground_y - self.size  # Place on ground
            self.v_y = 0.0  # Stop falling
            return True  # Hit ground
        return False  # Still in air

    def draw(self, screen: pygame.Surface):
        """Draw the body on the screen."""
        pygame.draw.rect(
            screen, self.settings.PLAYER_COLOR, (self.x, self.y, self.size, self.size)
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
        pygame.display.set_caption("Gravity and Jumping")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Create the player body
        start_x = self.settings.PLAYER_X
        start_y = self.settings.SCREEN_HEIGHT - self.settings.PLAYER_SIZE
        self.player = Body(start_x, start_y, self.settings.MASS, self.settings)

        # Game state
        self.is_jumping = False

    def update_physics(self):
        """Update the physics simulation."""
        # Continuously jump. If the player is not jumping, initialize a new jump
        if not self.is_jumping:
            self.player.jump(self.settings.JUMP_VELOCITY)
            self.is_jumping = True

        # Apply gravity
        self.player.apply_gravity(self.settings.GRAVITY)

        # Update the player's physics
        self.player.update()

        # Check for ground collision
        if self.player.check_ground_collision(self.settings.SCREEN_HEIGHT):
            self.is_jumping = False

    def draw(self):
        """Draw everything on the screen."""
        # Clear the screen
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the player
        self.player.draw(self.screen)

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