"""Game module."""

import random
import sys

import pygame
import pygame.sprite as sprite
from pygame.locals import *

from . import game_elements
from . import interface_elements

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

def handle_game_actions(ball, paddle, balls_barrier,score_board, screen):
    """Handles actions like collisions."""

    if targets_hit := sprite.spritecollide(ball, balls_barrier, True):
        score_board.points += len(targets_hit)
        score_board.update()
        ball.speedy *= -1
    # Checks the case of collisions between the ball and the paddle.
    if ball.rect.right >= ball.screen_rect.right:
        # Has collided on the right side, come back as it should.
        ball.speedx *= -1
        ball.current_colour = random.choice(ball.colours)
    elif ball.rect.left <= ball.screen_rect.left:
        # Has collided on the left side, come back as it should.
        ball.speedx *= -1
        ball.current_colour = random.choice(ball.colours)
    elif ball.rect.top <= ball.screen_rect.top:
        # Has collided on the top, come back as it should.
        ball.speedy *= -1
        ball.current_colour = random.choice(ball.colours)
    elif ball.rect.bottom > ball.screen_rect.bottom:
        # Restart the game
        ball.reset_pos()
        ball.speedy *= -1
        balls_barrier.empty()
        generate_barrier(balls_barrier, screen)
    #FIXME: Implement a better collision
    elif paddle.rect.colliderect(ball):
        ball.speedy *= -1


def generate_barrier(balls_barrier, screen):
    """Create a bunch of ball to get hit by the main ball."""

    balls_in_row = SCREEN_WIDTH // 30
    balls_in_column = SCREEN_HEIGHT // 30 - 10
    row = column = 0
    for r in range(balls_in_row):
        for c in range(balls_in_column):
            static_ball = game_elements.StaticBall(screen, row, column)
            static_ball.add(balls_barrier)
            column += 30
        column = 0
        row += 30


def main():
    """Main Program"""

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game. (With physics)")
    clock = pygame.time.Clock()

    # Game elements
    paddle = game_elements.Paddle(screen)
    ball = game_elements.Ball(screen)
    balls_barrier = sprite.Group()
    generate_barrier(balls_barrier, screen)

    # Interface elements
    score_board = interface_elements.ScoreBoard(screen)
    life_remaining_board = interface_elements.LifeRemaining(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
                pygame.quit()
            elif event.type == KEYDOWN:
                handle_keydown_events(event, paddle)
            elif event.type == KEYUP:
                handle_keyup_events(event, paddle)

        clock.tick(40)
        screen.fill((68, 68, 68))

        paddle.draw()
        ball.draw()
        score_board.draw()
        life_remaining_board.draw()
        balls_barrier.draw(screen)

        paddle.update()
        ball.update()
        handle_game_actions(ball, paddle, balls_barrier,score_board, screen)
        pygame.display.update()
