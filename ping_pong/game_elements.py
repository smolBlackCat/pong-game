"""Game elements module"""

import os
import random

import pygame
import pygame.sprite as sprite


class GameStats:
    """It's responsible for tracking the current the game is."""

    def __init__(self):
        self.running = False
        self.on_info = False
        self.paused = False
        self.game_over = False

    def is_running(self):
        return self.running

    def is_paused(self):
        return self.paused

    def is_on_info(self):
        return self.on_info

    def is_game_over(self):
        return self.game_over

    def set_running(self, v):
        self.running = v

    def set_on_info(self, v):
        self.on_info = v

    def set_paused(self, v):
        self.paused = v

    def set_game_over(self, v):
        self.game_over = v


class Paddle(sprite.Sprite):
    """Game's paddle."""

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load(os.path.join("game_assets", "images",
                                                    "paddle.png"))
        self.rect = self.image.get_rect()
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
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load(os.path.join("game_assets", "images",
                                                    "ball.png"))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.speedx = 5 * (random.choice((-1, 1)))
        self.speedy = -5

    def draw(self):
        """Draws the ball on the screen."""

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
        super().__init__()
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
