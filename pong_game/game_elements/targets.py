import os
import random

import pygame.sprite as sprite
import pygame.surface as surface

from .. import utils


class Target(sprite.Sprite):
    """Class that represents a literal target, the one that will
    be hit by the ball.
    """

    def __init__(self, screen):
        """Initialises the Target object. This object isn't used
        directly by the game but by the Targets class instead.
        
        Args:
        
            screen:
                A Surface object representing the window
                background.
        """

        sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = surface.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(Target.random_colour())
        self.image.blit(utils.load_image("on_game/target.png"), self.rect)
        
        self.vanish_soundfx = utils.load_soundfx(
            "on_game/soundfx/vanishing.wav")
        self.target_hit_soundfx = utils.load_soundfx(
            "on_game/soundfx/target_hit.wav")

        # Replaced with True when this target get hit
        self.falling = False

    @staticmethod
    def random_colour():
        """It generates a random colour to the target."""

        return [random.randint(0, 255) for _ in range(3)]

    def draw(self):
        """It draws the target on the screen."""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """It updates the current state of the target."""

        if self.rect.top > self.screen_rect.bottom:
            # Simply disappears. Stop rendering the hit target.
            self.kill()
            self.vanish_soundfx.play()
        elif self.falling:
            # Simulates falling effect
            self.rect.y += 1


class Targets:
    """A class that works as wrapper for a Group object."""

    def __init__(self, screen):
        """Initialises the Targets object.
        
        Args:
        
            screen:
                A Surface object representing the window
                background.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.group = sprite.Group()
        self.recharge()

    def draw(self):
        """It draws the targets on the screen."""

        self.group.draw(self.screen)

    @staticmethod
    def _collision_handling(ball, target):
        """Detects collision between the ball and a target.
        
        Args:
        
            ball:
                A Ball object that it's about to hit a target.
            
            target:
                A Target object that it's probably going to be hit
                by the ball unless the verification says otherwise.
        
        Returns

            A boolean value. Is True when the target is actually hit
            by the ball, otherwise False.
        """

        if ball.rect.colliderect(target.rect) and not target.falling:
            if abs(ball.rect.top - target.rect.bottom) < 10 \
                    and ball.yspeed < 0:
                ball.yspeed *= -1
            elif abs(ball.rect.bottom - target.rect.top) < 10 \
                    and ball.yspeed > 0:
                ball.yspeed *= -1
            elif abs(ball.rect.left - target.rect.right) < 10:
                ball.xspeed *= -1
            elif abs(ball.rect.right - target.rect.left) < 10:
                ball.xspeed *= -1
            target.target_hit_soundfx.play()
            return True
        return False

    def update(self, ball):
        """It updates the state of every single target in the
        group.

        Args:

            ball:
                A Ball object.
        """

        collided_targets = sprite.spritecollide(ball, self.group, False,
                                                Targets._collision_handling)
        for target in collided_targets:
            ball.points += 10000
            target.falling = True

        if len(self.group) == 0 and ball.y >= self.screen_rect.centery:
            # Recharge the targets when empty or the player failed in
            # catching the ball.
            self.recharge()

        self.group.update()

    def recharge(self):
        """It refills the group attribute with targets sprites."""

        # Making sure that the group is in fact empty.
        self.group.empty()

        rows = self.screen.get_width() // 32 + 1

        xpos = 0
        ypos = 0

        for y in range(5):
            for x in range(rows):
                target = Target(self.screen)
                target.rect.x = xpos
                target.rect.y = ypos
                self.group.add(target)
                xpos += 32
            ypos += 32
            xpos = 0
