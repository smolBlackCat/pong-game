import pygame.sprite as sprite

from .. import utils
from .particle import Particle


class Ball(sprite.Sprite):
    """Class that represents a literal ball. This ball is used on the
    game or anything else, like a demonstration.
    """

    def __init__(self, screen, free=False):
        """Initialises the Ball object.

        Args:

            screen:
                A Surface object representing the whole window
                background.

            free:
                A boolean value that indicates if the ball is in
                game mode, that is it's working like it's in the
                game. When False, it means that the ball is on a
                match.
        """
        sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = utils.load_image("on_game/ball.png")
        self.hit_soundfx = utils.load_soundfx("on_game/soundfx/ball_hit.ogg")
        self.rect = self.image.get_rect()

        self.xspeed = 2
        self.yspeed = 2

        self.points = 0

        # It stores a function. Its behaviour may change depeding on
        # the free arg.
        self.get_collision = None

        if free:
            def movement_logic(paddle, particles_group):
                if self.rect.left <= self.screen_rect.left \
                        or self.rect.right >= self.screen_rect.right:
                    self.xspeed *= -1
                    particles_group.append(Particle.create_particles(self.screen, self.rect.x, self.rect.y))
                if self.rect.top <= self.screen_rect.top \
                        or self.rect.bottom >= self.screen_rect.bottom:
                    self.yspeed *= -1
                    particles_group.append(Particle.create_particles(self.screen, self.rect.x, self.rect.y))

            self.get_collision = movement_logic
        else:
            def movement_logic(paddle, particles_group):
                if self.rect.left <= self.screen_rect.left or self.rect.right >= self.screen_rect.right:
                    self.hit_soundfx.play()
                    self.xspeed *= -1
                    particles_group.append(Particle.create_particles(self.screen, self.rect.x, self.rect.y))

                if self.rect.top <= self.screen_rect.top:
                    self.hit_soundfx.play()
                    self.yspeed *= -1
                    particles_group.append(Particle.create_particles(self.screen, self.rect.x, self.rect.y))

                if self.rect.colliderect(paddle.rect) and self.yspeed > 0:
                    self.hit_soundfx.play()
                    self.yspeed *= -1
            self.get_collision = movement_logic

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @x.setter
    def x(self, value):
        self.rect.x = value

    @y.setter
    def y(self, value):
        self.rect.y = value

    def draw(self):
        """It draws the ball on the surface."""

        self.screen.blit(self.image, self.rect)

    def update(self, paddle, particles_group):
        """It updates the movement of the ball.

        Args:

            paddle:
                A paddle (player) object where the rect attribute
                will be extracted.
        """

        self.x += self.xspeed
        self.y += self.yspeed

        # Movement logic
        self.get_collision(paddle, particles_group)
