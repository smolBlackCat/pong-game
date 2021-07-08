import pygame
import sys
from random import choice
from pygame.locals import *

pygame.init()


class Paddle:
    """Game's paddle."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, 100, 20)
        self.colour = (200, 200, 200)
        self.speed = 10

        # Sets paddle initial position
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.bottom - 20

        self.going_left = False
        self.going_right = False

    def draw(self):
        """Draws the paddle on the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)

    def update(self):
        """Updates the paddle position and another attributes."""
        if self.going_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        elif self.going_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.speed

class Ball:
    """Game's ball."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(300, 200, 30, 30)
        self.colours = [
            (4, 40, 77),
            (8, 175, 177),
            (8, 76, 145)
        ]
        self.current_colour = choice(self.colours)
        self.speedx = 5 * (choice((-1, 1)))
        self.speedy = 5 * (choice((-1, 1)))

    def draw(self):
        """Draws the ball on the screen."""

        pygame.draw.rect(self.screen, self.current_colour, self.rect)

    def update(self):
        """Updates the ball position and another attributes."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Checks the case of collisions
        if self.rect.right > self.screen_rect.right:
            # Has collided on the right side, come back as it should.
            self.speedx *= -1
            self.current_colour = choice(self.colours)
        elif self.rect.left < self.screen_rect.left:
            # Has collided on the left side, come back as it should.
            self.speedx *= -1
            self.current_colour = choice(self.colours)
        elif self.rect.top < self.screen_rect.top:
            # Has collided on the top, come back as it should.
            self.speedy *= -1
            self.current_colour = choice(self.colours)
        elif self.rect.bottom > self.screen_rect.bottom:
            # Has collided on the top, come back as it should.
            self.speedy *= -1
            self.current_colour = choice(self.colours)


# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400


def handle_keydown_events(event, paddle):
    """Handle all the buttons whether they are pressed."""
    if event.key == K_LEFT:
        paddle.going_left = True
    elif event.key == K_RIGHT:
        paddle.going_right = True


def handle_keyup_events(event, paddle):
    """Handles all the buttons whether they aren't pressed anymore."""
    if event.key == K_LEFT:
        paddle.going_left = False
    elif event.key == K_RIGHT:
        paddle.going_right = False


def main():
    """Main Program"""

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    paddle = Paddle(screen)
    ball = Ball(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
                pygame.quit()
            elif event.type == KEYDOWN:
                handle_keydown_events(event, paddle)
            elif event.type == KEYUP:
                handle_keyup_events(event, paddle)

        clock.tick(60)
        screen.fill((68, 68, 68))
        paddle.draw()
        paddle.update()
        ball.draw()
        ball.update()
        pygame.display.update()
