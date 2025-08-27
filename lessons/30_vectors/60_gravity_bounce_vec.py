"""
Gravity Bounce with Vectors

Simulates a ball bouncing under gravity using vectors.

uid: dos6D9jM
name: Gravity Bounce Vec
"""

from dataclasses import dataclass

import pygame
from orbitlib.colors import Colors


@dataclass
class Settings:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    BALL_RADIUS: int = 20
    BALL_COLOR = Colors.BLUE
    BACKGROUND_COLOR = Colors.WHITE
    GRAVITY: float = 0.5
    ELASTICITY: float = 0.8
    FPS: int = 60
    FONT_SIZE: int = 24


class Ball:
    def __init__(self, x, y):
        """Initializes the Ball with position and velocity vectors."""
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocity.y += Settings.GRAVITY
        self.position += self.velocity

        # Bounce off the floor
        if self.position.y + Settings.BALL_RADIUS > Settings.SCREEN_HEIGHT:
            self.position.y = Settings.SCREEN_HEIGHT - Settings.BALL_RADIUS
            self.velocity.y *= -Settings.ELASTICITY

        # Bounce off the walls
        if self.position.x - Settings.BALL_RADIUS < 0:
            self.position.x = Settings.BALL_RADIUS
            self.velocity.x *= -Settings.ELASTICITY
            
        elif self.position.x + Settings.BALL_RADIUS > Settings.SCREEN_WIDTH:
            self.position.x = Settings.SCREEN_WIDTH - Settings.BALL_RADIUS
            self.velocity.x *= -Settings.ELASTICITY

    def draw(self):
        pygame.draw.circle(
            screen,
            Settings.BALL_COLOR,
            (int(self.position.x), int(self.position.y)),
            Settings.BALL_RADIUS,
        )


class Simulation:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        global screen, clock, font
        screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Gravity Bounce with Vectors")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, self.settings.FONT_SIZE)
        self.ball = Ball(
            self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2
        )

    def update(self):
        self.ball.update()

    def draw(self):
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.ball.draw()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.velocity = pygame.math.Vector2(0, -15)
            self.update()
            self.draw()
            clock.tick(self.settings.FPS)
        pygame.quit()


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
