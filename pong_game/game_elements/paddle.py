import pygame


class Paddle:
    """Class that represents the player. Literally a white rectangle
    that hit the ball up.
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.base_colour = (255, 255, 255)
        self.line_colour = (0, 0, 0)

        self.rect = pygame.Rect(0, 0, 100, 20)

        self.moving_right = False
        self.moving_left = False
        self.speed = 3

    def draw(self):
        """It draws the paddle on the screen."""

        pygame.draw.rect(self.screen, self.line_colour, self.rect, width=4)
        pygame.draw.rect(self.screen, self.base_colour, self.rect)

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
