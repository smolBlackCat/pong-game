"""Module dedicated for putting backgrounds on scenes."""

import random

import pygame.sprite as sprite
import pygame.surface as surface

from .game_elements import target
from .game_elements.ball import Ball


class BaseBackground:
    """Base for background class."""

    def __init__(self, screen):
        """Initialises the object."""

        self.screen = screen
        self.screen_rect = screen.get_rect()

    def draw(self):
        """It draws the background."""

        pass

    def update(self):
        """It updates the background state."""

        pass


class GameBackground(BaseBackground):
    """A background that looks like exactly like the game
    dynamics.
    """

    def __init__(self, screen):
        super().__init__(screen)
        # Game elements (the user won't control these)
        self.ball = Ball(screen, True)
        self.targets = sprite.Group()
        target.recharge(screen, self.targets, True)

        self.ball.rect.center = self.screen_rect.center

    def draw(self):
        self.ball.draw()
        self.targets.draw(self.screen)

    def update(self):
        self.ball.update(None)
        self.targets.update(self.ball)


class ColourChangingBackground(BaseBackground):
    """A class that represents a Surface that changes its colour
    all the time.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.bg = surface.Surface(screen.get_size())
        self.colour = {
            "r": [random.randint(0, 255), 1],
            "g": [random.randint(0, 255), 1],
            "b": [random.randint(0, 255), 1]
        }

    def draw(self):
        r = self.colour["r"][0]
        g = self.colour["g"][0]
        b = self.colour["b"][0]
        self.screen.fill((r, g, b))

    def update(self):
        for key, colour_stats in self.colour.items():
            if colour_stats[0] >= 255:
                self.colour[key][1] = -1
            elif colour_stats[0] <= 0:
                self.colour[key][1] = 1

            self.colour[key][0] += self.colour[key][1]
