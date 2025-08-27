"""
vector20.py

Educational vector and grid visualization tools for teaching 2D vector concepts with pygame.

This module provides a Vector20 class (an extension of pygame.math.Vector2) and helper
drawing functions for displaying vectors and labeled grids on a pygame surface. It is
intended for classroom demonstration and student exploration, not for use in production games.
"""

import pygame
import math
from orbitlib.colors import Colors

# Constants for colors
WHITE = Colors.WHITE
BLACK = Colors.BLACK
BLUE = Colors.BLUE
GREEN = Colors.DARK_GREEN
GRAY = Colors.DARK_GRAY


# Factory function to create the Vector20 class with customizable screen size and scale
def Vector20Factory(screen_width=800, screen_height=600, scale=20):
    """
    Factory function to create the Vector20 class and associated drawing functions.

    Vector20 is an educational extension of pygame.math.Vector2 that represents a 2D vector
    and provides utilities for drawing vectors and labeled grids on a pygame surface.
    This is intended for teaching and visualization, not for use in production games.

    Args:
        screen_width (int): Width of the pygame window in pixels.
        screen_height (int): Height of the pygame window in pixels.
        scale (int): Number of pixels per grid unit.

    Returns:
        Vector20: The vector class.
        drawv20: Function to draw a vector on the grid.
        draw_grid: Function to draw the labeled grid.
    """

    class Vector20(pygame.math.Vector2):
        """
        An educational extension of pygame.math.Vector2 for grid-based visualization.

        This class represents a 2D vector and provides methods for drawing itself on a
        labeled grid using pygame. It is intended for teaching vector concepts, not for
        use in production games.

        Attributes:
            orig_x (float): The original x value (before scaling).
            orig_y (float): The original y value (before scaling).
        """

        def __init__(self, x=0, y=0):
            """
            Initialize a Vector20 object.

            Args:
                x (float): The x component of the vector (in grid units).
                y (float): The y component of the vector (in grid units).
            """
            # Calculate new x and y based on the center of the screen and scale
            scaled_x = x * scale
            scaled_y = -y * scale  # y is inverted to account for screen coordinates

            # Initialize the parent Vector2 with scaled values
            super().__init__(scaled_x, scaled_y)

            self.orig_x = x
            self.orig_y = y

    def drawv20(screen, start_o, end_o):
        """
        Draw a vector from start_o to end_o on the given pygame screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            start_o (Vector20): The starting vector (relative to origin).
            end_o (Vector20): The vector representing the displacement from start_o.

        Returns:
            pygame.math.Vector2: The end position relative to the screen origin.
        """
        # Draw the main line of the vector

        origin = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        start = origin + start_o
        end = end_o + start

        print("Draw from ", start, " to ", end)
        pygame.draw.line(screen, BLACK, start, end, 3)  # Line from start to end

        # Calculate the arrowhead
        arrow_length = 10  # Length of the arrowhead lines
        angle = math.atan2(end.y - start.y, end.x - start.x)  # Angle of the vector
        left_arrow = pygame.math.Vector2(
            end.x - arrow_length * math.cos(angle - math.pi / 6),
            end.y - arrow_length * math.sin(angle - math.pi / 6),
        )
        right_arrow = pygame.math.Vector2(
            end.x - arrow_length * math.cos(angle + math.pi / 6),
            end.y - arrow_length * math.sin(angle + math.pi / 6),
        )

        # Draw the arrowhead (two lines forming a 'V')
        pygame.draw.line(screen, BLACK, end, left_arrow, 3)
        pygame.draw.line(screen, BLACK, end, right_arrow, 3)

        # Calculate the midpoint
        mid_x = (start.x + end.x) / 2
        mid_y = (start.y + end.y) / 2

        # Create a font object
        font = pygame.font.SysFont(None, 24)

        disp_x = end_o.x // scale
        disp_y = end_o.y // scale

        # Render the text with white background
        text_surface = font.render(f"({disp_x:.1f}, {disp_y:.1f})", True, BLUE, WHITE)
        text_rect = text_surface.get_rect(center=(mid_x, mid_y))

        # Draw the text on the screen at the midpoint of the line
        screen.blit(text_surface, text_rect)

        return end - origin

    def _draw_grid(screen):
        """
        Draws the grid lines on the pygame screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        screen.fill(WHITE)  # Fill background with white

        # Calculate center
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Draw vertical lines
        for x in range(0, screen_width, scale):
            pygame.draw.line(screen, GRAY, (x, 0), (x, screen_height))
        # Draw horizontal lines
        for y in range(0, screen_height, scale):
            pygame.draw.line(screen, GRAY, (0, y), (screen_width, y))

        # Draw center lines in black
        pygame.draw.line(
            screen, GRAY, (center_x, 0), (center_x, screen_height), 2
        )  # vertical line
        pygame.draw.line(
            screen, GRAY, (0, center_y), (screen_width, center_y), 2
        )  # horizontal line

    def _label_lines(screen):
        """
        Draws the numeric labels for the grid lines.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        center_x = screen_width // 2
        center_y = screen_height // 2

        font = pygame.font.SysFont(None, 16)

        # Label vertical lines at y=0
        for x in range(0, screen_width, scale):
            line_number = (x - center_x) // scale
            if line_number != 0:  # Skip the center line label
                label = font.render(str(line_number), True, GREEN)
                label_rect = label.get_rect()
                # Draw the label with white background buffer
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        x - label_rect.width // 2,
                        center_y + 5,
                        label_rect.width,
                        label_rect.height,
                    ),
                )
                screen.blit(label, (x - label_rect.width // 2, center_y + 5))

        # Label horizontal lines at x=0
        for y in range(0, screen_height, scale):
            line_number = (center_y - y) // scale
            if line_number != 0:  # Skip the center line label
                label = font.render(str(line_number), True, GREEN)
                label_rect = label.get_rect()
                # Draw the label with white background buffer
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        center_x + 5,
                        y - label_rect.height // 2,
                        label_rect.width,
                        label_rect.height,
                    ),
                )
                screen.blit(label, (center_x + 5, y - label_rect.height // 2))

    def draw_grid(screen):
        """
        Draws the full grid and labels on the pygame screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        screen.fill(WHITE)
        _draw_grid(screen)
        _label_lines(screen)

    return Vector20, drawv20, draw_grid
