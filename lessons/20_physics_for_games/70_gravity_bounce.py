"""
Gravity Bounce with X Motion
If we add X velocity, from side to side, the player will bounce around the
screen. We will need to add a check to see if the player hits the left or right
side of the screen.

uid: IaZqWmy2
name: Gravity Bounce
"""

import pygame
from dataclasses import dataclass


@dataclass
class Settings:
    """Class to hold all game settings and constants."""

    # Screen settings
    SCREEN_WIDTH: int = 500
    SCREEN_HEIGHT: int = 500

    # Square settings
    SQUARE_SIZE: int = 20
    SQUARE_COLOR: tuple[int, int, int] = (0, 0, 0)  # Black

    # Physics settings
    GRAVITY: float = 60.0  # Gravitational acceleration (downward)
    JUMP_VELOCITY_Y: float = 200.0  # Initial upward velocity when jumping
    JUMP_VELOCITY_X: float = 100.0  # Initial horizontal velocity when jumping
    MASS: float = 2.0  # Mass of the square

    # Display settings
    BACKGROUND_COLOR: tuple[int, int, int] = (255, 255, 255)  # White
    FPS: int = 30

    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = 1.0 / self.FPS  # Time step for physics calculations


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
        self.size = settings.SQUARE_SIZE

    def apply_gravity(self, gravity: float):
        """Apply gravitational force (downward acceleration)."""
        self.a_y = gravity

    def jump(self, jump_velocity_y: float, jump_velocity_x: float):
        """Initiate a jump with both vertical and horizontal velocity."""
        self.v_y = (
            -jump_velocity_y
        )  # Negative because up is negative in screen coordinates
        self.v_x = jump_velocity_x

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

    def check_wall_collision(self, screen_width: float):
        """Check if the body hits the left or right walls and handle collision."""
        if self.x <= 0:
            self.x = 0
            self.v_x = -self.v_x  # Reverse horizontal velocity
            return True
        elif self.x + self.size >= screen_width:
            self.x = screen_width - self.size
            self.v_x = -self.v_x  # Reverse horizontal velocity
            return True
        return False

    def check_ceiling_collision(self):
        """Check if the body hits the ceiling and handle collision."""
        if self.y <= 0:
            self.y = 0
            self.v_y = -self.v_y  # Reverse vertical velocity
            return True
        return False

    def check_ground_collision(self, ground_y: float):
        """Check if the body hits the ground and handle collision."""
        if self.y + self.size >= ground_y:
            self.y = ground_y - self.size  # Place on ground
            self.v_y = 0.0  # Stop vertical motion
            self.v_x = 0.0  # Stop horizontal motion
            return True  # Hit ground
        return False  # Still in air

    def get_direction(self):
        """Get the current horizontal direction (1 for right, -1 for left, 0 for stationary)."""
        if self.v_x > 0:
            return 1
        elif self.v_x < 0:
            return -1
        else:
            return 0

    def draw(self, screen: pygame.Surface):
        """Draw the body on the screen."""
        pygame.draw.rect(
            screen, self.settings.SQUARE_COLOR, (self.x, self.y, self.size, self.size)
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
        pygame.display.set_caption("Gravity Bounce")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Create the bouncing square
        start_x = 100.0
        start_y = self.settings.SCREEN_HEIGHT - self.settings.SQUARE_SIZE
        self.square = Body(start_x, start_y, self.settings.MASS, self.settings)

        # Game state
        self.is_jumping = False
        self.x_direction = 1  # Track direction for next jump

    def update_physics(self):
        """Update the physics simulation."""
        # Continuously jump. If the square is not jumping, initialize a new jump
        if not self.is_jumping:
            jump_x = self.settings.JUMP_VELOCITY_X * self.x_direction
            self.square.jump(self.settings.JUMP_VELOCITY_Y, jump_x)
            self.is_jumping = True
        else:
            # Apply gravity while in the air
            self.square.apply_gravity(self.settings.GRAVITY)

        # Update the square's physics
        self.square.update()

        # Check for collisions
        # Wall collisions (reverse horizontal direction)
        if self.square.check_wall_collision(self.settings.SCREEN_WIDTH):
            self.x_direction = -self.x_direction  # Update direction for next jump

        # Ceiling collision
        self.square.check_ceiling_collision()

        # Ground collision (stop and prepare for next jump)
        if self.square.check_ground_collision(self.settings.SCREEN_HEIGHT):
            self.is_jumping = False

    def draw(self):
        """Draw everything on the screen."""
        # Clear the screen
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw the square
        self.square.draw(self.screen)

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