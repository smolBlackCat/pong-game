import pygame.sprite as sprite

from ..utils import load_image


class Paddle(sprite.Sprite):
    """Class that represents the player. Literally a white rectangle
    that hit the ball up.
    """

    def __init__(self, screen):
        """Initialises the Paddle object.
        
        Args:

            screen:
                A Surface object representing the window
                background.
        """

        sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = load_image("on_game/paddle.png")
        self.rect = self.image.get_rect()

        self.moving_right = False
        self.moving_left = False
        self.speed = 3

    def draw(self):
        """It draws the paddle on the screen."""

        self.screen.blit(self.image, self.rect)

    def move_left(self, moving: bool):
        self.moving_left = moving

    def move_right(self, moving: bool):
        self.moving_right = moving

    def update(self):
        """It updates the paddle state."""

        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left >= self.screen_rect.left:
            self.rect.x -= self.speed
