"""
Vector Rotations

Demonstrates rotating and scaling vectors on a labeled grid using Vector20.
This version uses a Settings dataclass, a Simulation class, and follows the
Python-OrbitLab style guide for structure and naming.

uid: NmAldWRh
name: Vector Rotations
"""

from dataclasses import dataclass

import pygame
from vector20 import Vector20Factory


@dataclass
class Settings:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    SCALE: int = 20
    FPS: int = 30
    BACKGROUND_COLOR = (255, 255, 255)
    WINDOW_TITLE: str = "Vector Rotations"


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
        Vector20, draw_v20, draw_grid = Vector20Factory(
            self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT, self.settings.SCALE
        )
        self.Vector20 = Vector20
        self.draw_v20 = draw_v20
        self.draw_grid = draw_grid

    def update(self):
        pass  # No dynamic update needed for static vector drawing

    def draw(self):
        self.draw_grid(self.screen)
        v0 = self.Vector20(0, 0)
        v1 = self.Vector20(0, 1) * 5
        v2 = self.Vector20(0, 1).rotate(135) * 10
        self.draw_v20(self.screen, v0, v1)
        self.draw_v20(self.screen, v0, v2)
        pygame.display.flip()

    def run(self):
        running = True
        self.draw()  # Draw once at start
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(self.settings.FPS)
        pygame.quit()


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()