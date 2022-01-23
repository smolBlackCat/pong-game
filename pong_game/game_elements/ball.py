import pygame


class Ball:
    """Class that represents a literal ball. This ball is used on the
    game or anything else, like a demonstration.
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.x = 0
        self.y = 0
        self.radius = 10

        self.base_colour = (255, 255, 255)
        self.line_colour = (0, 0, 0)

        self.xspeed = 2
        self.yspeed = 2

    def draw(self):
        """It draws the ball on the surface."""

        pygame.draw.circle(self.screen, self.line_colour, (self.x, self.y),
                           self.radius+1)
        pygame.draw.circle(self.screen, self.base_colour, (self.x, self.y),
                           self.radius)

    # TODO: Implement ball physics here
    def update(self):
        """It updates the movement of the ball."""
        self.x += self.xspeed
        self.y += self.yspeed

        # Movement logic
        if self.x <= self.screen_rect.left or self.x >= self.screen_rect.right:
            self.xspeed *= -1
        if self.y >= self.screen_rect.bottom or self.y <= self.screen_rect.top:
            self.yspeed *= -1
