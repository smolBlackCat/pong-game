import pygame.sprite as sprite
from .. import utils


class Ball(sprite.Sprite):
    """Class that represents a literal ball. This ball is used on the
    game or anything else, like a demonstration.
    """

    def __init__(self, screen):
        """Initialises the Ball object.
        
        Args:
        
            screen:
                A Surface object representing the whole window
                background.
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

    def update(self, paddle):
        """It updates the movement of the ball.
        
        Args:
        
            paddle:
                A paddle (player) object where the rect attribute
                will be extracted.
        """

        self.x += self.xspeed
        self.y += self.yspeed

        # Movement logic
        if self.rect.left <= self.screen_rect.left \
                or self.rect.right >= self.screen_rect.right:
            self.hit_soundfx.play()
            self.xspeed *= -1
        if self.rect.top <= self.screen_rect.top:
            self.hit_soundfx.play()
            self.yspeed *= -1

        if self.rect.colliderect(paddle.rect) and self.yspeed > 0:
            self.hit_soundfx.play()
            self.yspeed *= -1
