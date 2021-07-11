"""Game elements module"""

import random

import pygame
import pygame.sprite as sprite


class Paddle(sprite.Sprite):
    """Game's paddle."""

    def __init__(self, screen):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100, 20))
        self.rect = self.image.get_rect()
        self.colour = (200, 200, 200)
        self.image.fill(self.colour)
        self.speed = 10

        # Sets paddle initial position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = self.screen_rect.bottom - 20

        self.going_left = False
        self.going_right = False

    def draw(self):
        """Draws the game's paddle on the screen."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updates the paddle position and another attributes."""
        if self.going_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        elif self.going_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.speed

class Ball(sprite.Sprite):
    """Game's ball."""

    def __init__(self, screen):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((30, 30))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

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

        self.image.fill(self.current_colour)
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updates the ball position and another attributes."""

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def reset_pos(self):
        """Updates the position to the initial positon that the ball
        started."""

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery


class StaticBall(sprite.Sprite):
    """Similar to the Ball, but this time it's static. Will serve as a
    target."""

    def __init__(self, screen, posx, posy):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.colour = (random.randint(0,255), random.randint(0,255),
                       random.randint(0,255))
        self.image = pygame.Surface((30, 30))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def draw(self):
        """Draw the static ball on the screen."""

        self.screen.blit(self.image, self.rect)
