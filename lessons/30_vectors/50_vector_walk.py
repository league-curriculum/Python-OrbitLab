"""
Vector Walk - Object Oriented Version
Demonstrates moving a player using a direction vector, with rotation and scaling,
displaying vector information. Follows the Python-OrbitLab style guide for structure and naming.
"""

from dataclasses import dataclass

import pygame


@dataclass
class Settings:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    PLAYER_SIZE: int = 20
    LINE_COLOR = (0, 255, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    FPS: int = 30
    ANGLE_CHANGE: int = 3
    LENGTH_CHANGE: int = 5
    INITIAL_LENGTH: int = 100
    FONT_SIZE: int = 24


class Player:
    def __init__(self, x, y):
        """Initializes the Player with a position and direction vector."""

        self.position = pygame.math.Vector2(x, y)
        self.direction_vector = pygame.math.Vector2(Settings.INITIAL_LENGTH, 0)

        self.moves = []

    def update(self):
        pass  # No continuous update needed; movement is event-driven

    def draw(self, screen, show_line=True):
        pygame.draw.rect(
            screen,
            Settings.PLAYER_COLOR,
            (
                self.position.x - Settings.PLAYER_SIZE // 2,
                self.position.y - Settings.PLAYER_SIZE // 2,
                Settings.PLAYER_SIZE,
                Settings.PLAYER_SIZE,
            ),
        )

        if show_line:
            if self.moves:
                end_position = self.moves[-1]
            else:
                end_position = self.position + self.direction_vector

            pygame.draw.line(
                screen, Settings.LINE_COLOR, self.position, end_position, 2
            )

    def calc_moves(self):
        """Calc steps to move the player along the
        direction vector in N steps (no rendering or timing)."""

        final_position = self.position + self.direction_vector

        length = self.direction_vector.length()

        N = int(length // 3)
        if N == 0:
            return
        step = (final_position - self.position) / N
        pos = self.position.copy()

        for _ in range(N):
            pos += step
            self.moves.append(pos.copy())

    def move(self):
        if self.moves:
            self.position = self.moves.pop(0)

        if not self.moves:
            return False
        else:
            return True

    def hasMoves(self):
        return len(self.moves) > 0


class Simulation:
    def __init__(self):
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, self.settings.FONT_SIZE)

        self.player = Player(
            self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2
        )

    def update(self):
        pass  # All updates are event-driven

    def draw(self):
        self.screen.fill(self.settings.BACKGROUND_COLOR)
        self.player.draw(self.screen)

        self.draw_text()

        pygame.display.flip()

    def draw_text(self):
        direction_x, direction_y = (
            self.player.direction_vector.x,
            self.player.direction_vector.y,
        )

        vector_text = f"Vector: ({direction_x:.2f}, {direction_y:.2f})"
        vector_surface = self.font.render(vector_text, True, Settings.TEXT_COLOR)
        self.screen.blit(vector_surface, (10, Settings.SCREEN_HEIGHT - 70))

        magnitude = self.player.direction_vector.length()
        magnitude_text = f"Magnitude: {magnitude:.2f}"
        magnitude_surface = self.font.render(magnitude_text, True, Settings.TEXT_COLOR)
        self.screen.blit(magnitude_surface, (10, Settings.SCREEN_HEIGHT - 45))

        angle = self.player.direction_vector.angle_to(pygame.math.Vector2(1, 0))
        angle_text = f"Angle: {angle:.2f}\u00b0"
        angle_surface = self.font.render(angle_text, True, Settings.TEXT_COLOR)
        self.screen.blit(angle_surface, (10, Settings.SCREEN_HEIGHT - 20))

    def run(self):
        pygame.init()
        pygame.display.set_caption("Player with Direction Vector")

        running = True
        pygame.key.set_repeat(50, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            if self.player.hasMoves():
                # Move the player along the vector.
                self.player.move()

            else:
                if keys[pygame.K_LEFT]:
                    self.player.direction_vector = self.player.direction_vector.rotate(
                        -self.settings.ANGLE_CHANGE
                    )
                elif keys[pygame.K_RIGHT]:
                    self.player.direction_vector = self.player.direction_vector.rotate(
                        self.settings.ANGLE_CHANGE
                    )

                if keys[pygame.K_UP]:
                    self.player.direction_vector.scale_to_length(
                        self.player.direction_vector.length()
                        + self.settings.LENGTH_CHANGE
                    )

                elif keys[pygame.K_DOWN]:
                    self.player.direction_vector.scale_to_length(
                        self.player.direction_vector.length()
                        - self.settings.LENGTH_CHANGE
                    )

                elif keys[pygame.K_SPACE]:
                    self.player.calc_moves()

            self.draw()

            self.clock.tick(self.settings.FPS)

        pygame.quit()


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
