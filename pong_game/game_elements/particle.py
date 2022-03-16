"""Module created for dealing with particles."""

import random

import pygame.sprite as sprite
from .. import utils


class Particle(sprite.Sprite):
    """Class that represents a tiny particle coming from hit walls
    or targets."""

    def __init__(self, screen, x_pos, y_pos):
        """Initialises the Particle object.

        Args:

            xpos:
                X position.

            ypos:
                Y position.
        """

        super().__init__()
        self.screen_rect = screen.get_rect()
        self.image = utils.load_image("on_game/particle.png")
        self.rect = self.image.get_rect()

        self.accel_factor = random.randint(1, 4)

        self.xspeed = random.choice([-1, 1])*random.randint(1, 6)
        self.yspeed = 4

        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        """It updates the particle movement."""

        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        self.yspeed += self.accel_factor

        if self.rect.bottom > self.screen_rect.bottom:
            self.kill()

    @staticmethod
    def create_particles(screen, x_pos, y_pos):
        """Creates a Group of particles.

        Args:

            screen:
                A Surface object representing the window's surface.

            xpos:
                X position.

            ypos:
                Y position.
        """

        group = sprite.Group()

        for i in range(10):
            group.add(Particle(screen, x_pos, y_pos))

        return group
