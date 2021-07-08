"""Game module."""
import sys

import pygame
from pygame.locals import *

from . import game_elements

pygame.init()


# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400


def handle_keydown_events(event, paddle):
    """Handle all the buttons whether they are pressed."""
    if event.key == K_LEFT:
        paddle.going_left = True
    elif event.key == K_RIGHT:
        paddle.going_right = True


def handle_keyup_events(event, paddle):
    """Handles all the buttons whether they aren't pressed anymore."""
    if event.key == K_LEFT:
        paddle.going_left = False
    elif event.key == K_RIGHT:
        paddle.going_right = False


def main():
    """Main Program"""

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game. (With physics)")
    clock = pygame.time.Clock()
    paddle = game_elements.Paddle(screen)
    ball = game_elements.Ball(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
                pygame.quit()
            elif event.type == KEYDOWN:
                handle_keydown_events(event, paddle)
            elif event.type == KEYUP:
                handle_keyup_events(event, paddle)

        clock.tick(60)
        screen.fill((68, 68, 68))
        paddle.draw()
        paddle.update()
        ball.draw()
        pygame.display.update()
