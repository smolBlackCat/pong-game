"""Game module."""

import random
import sys

import pygame
import pygame.sprite as sprite
import pygame.font as font
from pygame.locals import *

from . import game_elements
from . import interface_elements

pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400


def handle_keydown_events(game_stats, event, paddle):
    """Handle all the buttons whether they are pressed."""

    if event.key == K_LEFT:
        paddle.going_left = True
    elif event.key == K_RIGHT:
        paddle.going_right = True
    elif event.key == K_p and not game_stats.is_game_over():
        game_stats.set_paused(not game_stats.is_paused())


def handle_keyup_events(event, paddle):
    """Handles all the buttons whether they aren't pressed anymore."""

    if event.key == K_LEFT:
        paddle.going_left = False
    elif event.key == K_RIGHT:
        paddle.going_right = False


def handle_game_actions(game_stats, ball, paddle, balls_barrier, score_board,
                        remaining_life, screen):
    """Handles actions like collisions."""

    if targets_hit := sprite.spritecollide(ball, balls_barrier, True):
        score_board.points += len(targets_hit)
        score_board.update()
        ball.speedy *= -1
    # Checks the case of collisions between the ball and the paddle.
    if ball.rect.right >= ball.screen_rect.right:
        # Has collided on the right side, come back as it should.
        ball.speedx *= -1
    elif ball.rect.left <= ball.screen_rect.left:
        # Has collided on the left side, come back as it should.
        ball.speedx *= -1
    elif ball.rect.top <= ball.screen_rect.top:
        # Has collided on the top, come back as it should.
        ball.speedy *= -1
    elif ball.rect.bottom > ball.screen_rect.bottom:
        # Restart the game
        if len(remaining_life.group) == 0:
            game_stats.set_game_over(True)
            return
        ball.reset_pos()
        ball.speedy *= -1
        balls_barrier.empty()
        generate_barrier(balls_barrier, screen)
        remaining_life.poll()
    elif paddle.rect.colliderect(ball) and ball.speedy > 0:
        ball.speedy *= -1
    elif len(balls_barrier) == 0:
        generate_barrier(balls_barrier, screen)


def restart_game(screen, ball, balls_barrier, life_remaining_board):
    ball.reset_pos()
    ball.speedy *= -1
    balls_barrier.empty()
    generate_barrier(balls_barrier, screen)
    life_remaining_board.fill()


def show_pause_message(screen):
    """Shows the pause message to the user, where s/he has the option
    to return to the game or return to the main menu.
    """

    text_font = font.SysFont("Arial", bold=True, size=14)
    text_colour = (114,137,218)
    rendered_text = text_font.render("PAUSE", False, text_colour)
    text_rect = rendered_text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery

    screen.blit(rendered_text, text_rect)


def show_game_over_message(game_stats, screen, ball, balls_barrier,
                           life_remaining_board):
    """Shows the game over message and gives the user the options to
    try again or to return to the main menu.
    """

    pygame.mouse.set_visible(True)
    text_font = font.SysFont("Arial", bold=True, size=14)
    game_over_colour = (214, 45, 32)
    try_again_colour = (0, 135, 68)

    centerx = screen.get_rect().centerx
    centery = screen.get_rect().centery

    game_over = text_font.render("GAME OVER", False, game_over_colour)
    game_over_rect = game_over.get_rect()
    game_over_rect.centerx = centerx
    game_over_rect.centery = centery

    try_again_button = interface_elements.Button(
        screen, try_again_colour, "TRY AGAIN", centerx - 120,
        centery + 40, lambda: game_stats.set_game_over(False),
        lambda: restart_game(screen, ball, balls_barrier, life_remaining_board)
    )
    main_menu_button = interface_elements.Button(
        screen, game_over_colour, "MAIN MENU", centerx + 40,
        centery + 40, lambda:game_stats.set_game_over(False),
        lambda: restart_game(screen, ball, balls_barrier, life_remaining_board),
        lambda: game_stats.set_running(False)
    )

    screen.blit(game_over, game_over_rect)
    try_again_button.draw()
    main_menu_button.draw()

    try_again_button.update()
    main_menu_button.update()


def show_game_info(game_stats, screen):
    """Shows the game instructions to the user."""

    game_stats.set_on_info(True)

    title_text_font = font.SysFont("Arial", bold=True, size=16)
    title_colour = (255, 255, 255)
    message_text_font = font.SysFont("Arial", bold=True, size=12)
    message_colour = (190, 190, 190)

    paddle_title = title_text_font.render("Paddle:", True, title_colour)
    paddle_title_rect = paddle_title.get_rect()
    paddle_title_rect.topleft = screen.get_rect().topleft
    paddle_title_rect.x += 20
    paddle_title_rect.y += 40
    paddle_message = message_text_font.render(
        "The key right and left arrows moves the paddle across the screen.",
        True, message_colour
    )
    paddle_message_rect = paddle_message.get_rect()
    paddle_message_rect.centerx = screen.get_rect().centerx
    paddle_message_rect.centery = screen.get_rect().centery - 90
    objective_title = title_text_font.render("Objective", True, title_colour)
    objective_rect = objective_title.get_rect()
    objective_rect.topleft = screen.get_rect().topleft
    objective_rect.y += 150
    objective_rect.x += 20
    objective_texts = []
    texts = [
        "Your only objective is to hit all the targets (the coloured balls)",
        "You have 3 lives, if you lost every single one of them, "
        +"then you die...", "I mean, you lose the game."
    ]
    padding = 0
    for text in texts:
        current = message_text_font.render(text, True, message_colour)
        current_rect = current.get_rect()
        current_rect.x = 40
        current_rect.y = 225 + padding
        objective_texts.append((current, current_rect))
        padding += current.get_height()

    # Paddle info
    screen.blit(paddle_title, paddle_title_rect)
    screen.blit(paddle_message, paddle_message_rect)

    # Objective info
    screen.blit(objective_title, objective_rect)
    for objective_text, objective_text_rect in objective_texts:
        screen.blit(objective_text, objective_text_rect)

    # Button to return to the main menu
    return_button = interface_elements.Button(
        screen, (0, 0, 68), "RETURN TO THE MAIN MENU",
        screen.get_rect().centerx, screen.get_rect().bottom - 40,
        lambda: game_stats.set_on_info(False)
    )
    return_button.draw()
    return_button.update()


def show_main_menu(game_stats, screen):
    """Shows the game main menu."""

    if not game_stats.is_on_info():
        text_font = font.SysFont("Arial", bold=True, size=16)
        colour = (255, 255, 255)
        red = (69, 0, 0)

        rendered_title_text = text_font.render("North-east Science:", True, colour)
        rendered_title_text2 = text_font.render("Pong Game", True, colour)

        centerx = screen.get_rect().centerx
        centery = screen.get_rect().centery

        title_rect = rendered_title_text.get_rect()
        title_rect.centerx = centerx
        title_rect.centery = centery - 150

        title2_rect = rendered_title_text2.get_rect()
        title2_rect.centerx = title_rect.centerx
        title2_rect.centery = centery - 90

        # Main Menu title
        screen.blit(rendered_title_text, title_rect)
        screen.blit(rendered_title_text2, title2_rect)

        start_button = interface_elements.Button(
            screen, red, "START", centerx-40, centery+40,
            lambda: game_stats.set_running(True),
            lambda:pygame.mouse.set_visible(False)
        )
        info_button = interface_elements.Button(
            screen, red, "HOW TO PLAY", centerx-40, centery+80,
            lambda: show_game_info(game_stats, screen)
        )
        start_button.draw()
        info_button.draw()
        start_button.update()
        info_button.update()
    else:
        show_game_info(game_stats, screen)

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

    # Game basics
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game. (With physics)")
    clock = pygame.time.Clock()
    

    # Game elements
    game_stats = game_elements.GameStats()
    paddle = game_elements.Paddle(screen)
    ball = game_elements.Ball(screen)
    balls_barrier = sprite.Group()
    generate_barrier(balls_barrier, screen)

    # Interface elements
    score_board = interface_elements.ScoreBoard(screen)
    life_remaining_board = interface_elements.LifeRemaining(screen)
    blocks_rain = interface_elements.BlockRain(screen)

    pygame.mouse.set_visible(True)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                handle_keydown_events(game_stats, event, paddle)
            elif event.type == KEYUP:
                handle_keyup_events(event, paddle)

        clock.tick(40)
        screen.fill((68, 68, 68))
        if game_stats.is_running():
            paddle.draw()
            ball.draw()
            score_board.draw()
            life_remaining_board.draw()
            balls_barrier.draw(screen)
            if game_stats.is_paused():
                # Code that pauses the game and show a pause message.
                show_pause_message(screen)
            elif game_stats.is_game_over():
                # Code stops the game and show a game over message
                show_game_over_message(game_stats, screen, ball, balls_barrier,
                                       life_remaining_board)
            else:
                paddle.update()
                ball.update()
                handle_game_actions(game_stats, ball, paddle, balls_barrier,
                                    score_board, life_remaining_board, screen)
        else:
            blocks_rain.draw()
            blocks_rain.update()
            show_main_menu(game_stats, screen)
        pygame.display.update()
