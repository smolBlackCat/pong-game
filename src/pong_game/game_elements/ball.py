import pygame.sprite as sprite

from core import utils
from core.effects import Particle

from .. import assets_path


class Ball(sprite.Sprite):
    """Class that represents a literal ball. This ball is used on the
    game or anything else, like a demonstration.
    """

    def __init__(self, screen, on_game=True):
        """Initialises the Ball object.

        Args:

            screen:
                A Surface object representing the whole window
                background.

            on_game:
                A boolean value that indicates if this ball is in
                actual game.
        """

        sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.on_game = on_game

        self.image = utils.load_image(f"{assets_path}/on_game/ball.png")
        self.hit_soundfx = utils.load_soundfx(f"{assets_path}/on_game/soundfx/ball_hit.ogg", 0.2)
        self.rect = self.image.get_rect()

        self.xspeed = 2
        self.yspeed = 2

        self.points = 0

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

    def check_wall_collision(self, particles_group):
        """Checks for wall collisions.

        Args:

            particles_group:
                A list object containing groups of particles to be
                drawn onto screen.
        """

        if self.rect.left <= self.screen_rect.left \
                or self.rect.right >= self.screen_rect.right:

            if self.on_game:
                self.hit_soundfx.play()

            self.xspeed *= -1
            particles = Particle.create_particles(
                self.screen,
                utils.load_image(f"{assets_path}/on_game/particle.png"),
                self.rect.x, self.rect.y)
            particles_group.append(particles)
        elif self.rect.top <= self.screen_rect.top \
                or (self.rect.bottom >= self.screen_rect.bottom
                    and not self.on_game):

            if self.on_game:
                utils.play_soundfx(self.hit_soundfx)

            self.yspeed *= -1
            particles = Particle.create_particles(
                self.screen,
                utils.load_image(f"{assets_path}/on_game/particle.png"),
                self.rect.x, self.rect.y)
            particles_group.append(particles)

    def check_paddle_collision(self, paddle):
        """Checks a paddle collision.

        Args:

            paddle:
                A Paddle object that is the player.
        """

        if self.rect.colliderect(paddle.rect) and self.yspeed > 0:
            self.hit_soundfx.play()
            self.yspeed *= -1

    def update(self, particles_group, paddle=None):
        """It updates the movement of the ball.

        Args:

            particles_group:
                A list object with groups of particles.

            paddle:
                A Paddle (player) object. Use None when this ball
                isn't in a game.
        """

        self.x += self.xspeed
        self.y += self.yspeed

        # Movement logic
        self.check_wall_collision(particles_group)

        if paddle is not None:
            self.check_paddle_collision(paddle)
