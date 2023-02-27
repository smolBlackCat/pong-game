"""Module for various effects."""

import random

import pygame.sprite as sprite
import pygame.surface as surface


class Particle(sprite.Sprite):
    """Particle class."""

    def __init__(self, screen: surface.Surface, image: surface.Surface,
                 x_pos: int, y_pos: int):
        """Initialises the Particle object.

        Args:
            screen: Game window surface.

            image: Any Surface object. It can be obtained from an
                   image or created by instantiating a Surface object.

            xpos: X position.

            ypos: Y position.
        """

        super().__init__()
        self.screen_rect = screen.get_rect()
        self.image = image
        self.rect = self.image.get_rect()

        self.accel_factor = random.randint(1, 4)

        self.xspeed = random.choice([-1, 1])*random.randint(1, 6)
        self.yspeed = 4

        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self) -> None:
        """Updates the particle movement."""

        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        self.yspeed += self.accel_factor

        # Kill the particle when it's not visible on the screen
        if self.rect.bottom > self.screen_rect.bottom \
                or self.rect.top < self.screen_rect.top \
                or self.rect.left > self.screen_rect.left \
                or self.rect.right < self.screen_rect.right:
            self.kill()

    @staticmethod
    def create_particles(screen: surface.Surface, image: surface.Surface,
                         x_pos: int, y_pos: int) -> sprite.Group:
        """Creates a Group of particles.

        Args:

            screen: Surface object representing the window's surface.

            xpos: X position.

            ypos: Y position.
        """

        group = sprite.Group()
        for i in range(10):
            group.add(Particle(screen, image, x_pos, y_pos))

        return group


def floating_animation(component, y_bottom: int, y_top: int) -> None:
    """Simulates a floating object with a given sprite rect.

    This won't animate a complete floating animation as it's a step
    of the animation rather than the whole process. This function must
    be used within the main loop.

    Args:

        component: Any graphical component that has rect attribute.

        y_bottom: where the component will start floating.

        y_top: where the component will stop ascending and then go
               back to the initial point.
    """

    if component.rect.bottom >= y_bottom \
            or component.rect.top <= y_top:
        component.yspeed *= -1
    component.rect.y += component.yspeed
