import random

import pygame.sprite as sprite
import pygame.surface as surface

from .. import utils
from .particle import Particle


class Target(sprite.Sprite):
    """Class that represents a literal target, the one that will
    be hit by the ball.
    """

    def __init__(self, screen, on_game=True):
        """Initialises the Target object. This object isn't used
        directly by the game but by the Targets class instead.

        Args:

            screen:
                A Surface object representing the window
                background.

            on_game:
                A boolean value that indicates if the target is on a
                match.
        """

        sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.on_game = on_game

        self.image = surface.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill([random.randint(0, 255) for i in range(3)])
        self.image.blit(utils.load_image("on_game/target.png"), self.rect)

        self.vanish_soundfx = utils.load_soundfx(
            "on_game/soundfx/vanishing.wav")
        self.target_hit_soundfx = utils.load_soundfx(
            "on_game/soundfx/target_hit.wav")

        # Replaced with True when this target get hit
        self.falling = False

    def collision(self, ball, particles_group):
        if ball.rect.colliderect(self.rect) and not self.falling:
            if abs(ball.rect.top - self.rect.bottom) < 10 \
                    and ball.yspeed < 0:
                ball.yspeed *= -1
            elif abs(ball.rect.bottom - self.rect.top) < 10 \
                    and ball.yspeed > 0:
                ball.yspeed *= -1
            elif abs(ball.rect.left - self.rect.right) < 10:
                ball.xspeed *= -1
            elif abs(ball.rect.right - self.rect.left) < 10:
                ball.xspeed *= -1
            if self.on_game:
                self.target_hit_soundfx.play()

            particles = Particle.create_particles(self.screen, self.rect.x,
                                                  self.rect.y)
            particles_group.append(particles)
            return True
        return False

    def update(self, ball, particles_group):
        """It updates the current state of the target."""

        if self.rect.top > self.screen_rect.bottom:
            # Simply disappears. Stop rendering the hit target.
            self.kill()
            if not self.on_game:
                self.vanish_soundfx.play()
        elif self.falling:
            # Simulates falling effect
            self.rect.y += 1

        if self.collision(ball, particles_group):
            ball.points += 100
            self.falling = True


def update(screen, screen_rect, targets, ball, on_game, particles_group):
    """It updates the state of every single target in the
    group.

    Args:

        screen:
            A Surface object representing the game window.
        
        screen_rect:
            A Rect object obtained from the screen's surface.
        
        targets:
            A Group object filled with Target(s).
        
        ball:
            A Ball object. The actual player.
        
        on_game:
            Boolean value that indicates if the targets to be created
            are going to be in a match.
        
        particles_group:
            A list object containing Group(s) of Particle(s).
    """

    if len(targets) == 0 and ball.y >= screen_rect.centery:
        # Recharge the targets when empty or the player failed in
        # catching the ball.
        recharge(screen, targets, on_game)

    targets.update(ball, particles_group)


def recharge(screen, targets, on_game=True):
    """It refills the group attribute with targets sprites."""

    # Making sure that the group is in fact empty.
    targets.empty()

    rows = 600 // 32 + 1

    xpos = 0
    ypos = 0

    for y in range(5):
        for x in range(rows):
            target = Target(screen, on_game)
            target.rect.x = xpos
            target.rect.y = ypos
            targets.add(target)
            xpos += 32
        ypos += 32
        xpos = 0
