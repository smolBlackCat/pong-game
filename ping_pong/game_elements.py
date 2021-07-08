"""Game elements module"""

import random

import pygame
import pygame.sprite as sprite


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
        self.colours = []
        for c in range(10):
            colour = (random.randint(0, 255), random.randint(0, 255),
                      random.randint(0, 255))
            self.colours.append(colour)
        self.current_colour = random.choice(self.colours)
        self.speedx = 5 * (random.choice((-1, 1)))
        self.speedy = -5

    def draw(self):
        """Draws the ball on the screen."""

        pygame.draw.rect(self.screen, self.current_colour, self.rect)

    def update(self, paddle):
        """Updates the ball position and another attributes."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Checks the case of collisions
        if self.rect.right > self.screen_rect.right:
            # Has collided on the right side, come back as it should.
            self.speedx *= -1
            self.current_colour = random.choice(self.colours)
        elif self.rect.left < self.screen_rect.left:
            # Has collided on the left side, come back as it should.
            self.speedx *= -1
            self.current_colour = random.choice(self.colours)
        elif self.rect.top < self.screen_rect.top:
            # Has collided on the top, come back as it should.
            self.speedy *= -1
            self.current_colour = random.choice(self.colours)
        elif self.rect.colliderect(paddle):
            self.speedy *= -1


class StaticBalls(Ball, sprite.Sprite):
    """Similar to the Ball, but this time it's static. Will serve as a
    target."""

    def __init__(self, screen, posx, posy):
        super().__init__(screen)
        sprite.Sprite.__init__(self)

        self.current_colour = random.choice(self.colours)
        self.rect.x = posx
        self.rect.y = posy

    def draw(self):
        """Draw the static ball on the screen."""
        pygame.draw.rect(self.screen, self.current_colour, self.rect)

    def update(self):
        """Does nothing. After all, it's a static ball."""
        return None
