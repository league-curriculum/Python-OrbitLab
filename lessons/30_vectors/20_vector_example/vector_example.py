"""
Vector Example

Demonstrates drawing a sequence of vectors on a labeled grid using Vector20.

uid: 7OQwInzg
name: Vector Example
"""

import pygame
from vector20 import Vector20Factory
from dataclasses import dataclass
from orbitlib.colors import Colors


@dataclass
class Settings:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    SCALE: int = 20
    FPS: int = 30
    BACKGROUND_COLOR = Colors.WHITE
    WINDOW_TITLE: str = "Vector Example"


Vector20, draw_v20, draw_grid = Vector20Factory(
    Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, Settings.SCALE
)

class Simulation:
    """Class to handle the main simulation loop and vector drawing."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()


    def update(self):
        pass  # No dynamic update needed for static vector drawing

    def draw(self):
        
        draw_grid(self.screen)

        start = Vector20(0, 0) # Origin 

        vectors = [
            Vector20(8, 8),
            Vector20(3, -12),
            Vector20(-4, -2),
            Vector20(-12, 0),
            Vector20(0, 12),
        ]

        for v in vectors:
            start = draw_v20(self.screen, start, v)

        pygame.display.flip()

    def run(self):
        
        running = True
        
        self.draw()  # Draw once at start


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.quit()


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
