import pygame.constants as constants
import pygame.draw as draw
import pygame.rect as rect
import pygame.sprite as sprite
import pygame.surface as surface
import pygame.time as time

from core import effects, interface, transition, utils
from core.scene import Scene

from . import assets_path
from .background import ColourChangingBackground, GameBackground
from .game_elements import target
from .game_elements.ball import Ball
from .game_elements.paddle import Paddle


class DebugScene(Scene):
    """Simple scene class that displays a white background. Mainly
    used to debug new stuff.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.bg = surface.Surface(self.screen.get_size())
        self.bg.fill((200, 200, 200))

        self.rect = self.bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Do whatever you want here
        self.test_rect = rect.Rect(0, 0, 10, 10)
        self.test_rect.center = self.screen_rect.center

    def draw(self):
        self.screen.blit(self.bg, self.rect)
        draw.rect(self.screen, (0, 0, 180), self.test_rect)


# TODO: Find a safer way of timing stuff. Sending events is proper to
# fail


class IntroScene(Scene):
    """A scene that shows the logo of the creator of the game."""

    END_INTRO = constants.USEREVENT + 1

    def __init__(self, screen):
        super().__init__(screen)

        self.logo_icon = interface.Label(
            screen, utils.load_image(f"{assets_path}/game_intro/moura_cat.png"))
        self.logo_title = interface.Label(
            screen, utils.load_image(f"{assets_path}/game_intro/logo_title.png"))

        self.logo_icon.rect.centerx = self.screen_rect.centerx
        self.logo_icon.rect.centery = self.screen_rect.centery

        self.logo_title.rect.centerx = self.screen_rect.centerx
        self.logo_title.rect.centery = self.screen_rect.centery + 74

        time.set_timer(IntroScene.END_INTRO, 3000, 1)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.logo_icon.draw()
        self.logo_title.draw()

    def update_on_event(self, event):
        if event.type == IntroScene.END_INTRO:
            print("changing view")
            self.scene_manager.change_scene(
                "main_menu",
                transition.FadeTransition(
                    self.screen, self.scene_manager, "main_menu",
                    (0, 0, 0), 4))


class MainMenuScene(Scene):
    """A scene that shows the "game" main menu."""

    def __init__(self, screen):
        super().__init__(screen)

        self.background = GameBackground(screen)

        self.game_title = interface.Label(
            screen, utils.load_image(
                f"{assets_path}/main_menu/game_title.png"),
            effects.floating_animation, 120, self.screen_rect.top)

        def play_button_action():
            fadefx = transition.FadeTransition(
                self.screen, self.scene_manager, "on_game", (255, 255, 255))
            self.scene_manager.change_scene(
                "on_game", fadefx)

            # Always get brand new game
            self.scene_manager.views["on_game"].retry()

        self.play_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/main_menu/play_button_on.png"),
            utils.load_image(f"{assets_path}/main_menu/play_button_off.png"),
            utils.load_image(
                f"{assets_path}/main_menu/play_button_clicked.png"),
            play_button_action)

        def settings_button_action():
            fadefx = transition.FadeTransition(
                self.screen, self.scene_manager, "on_settings", (255, 255, 255))
            self.scene_manager.change_scene("on_settings", fadefx)

        self.settings_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/main_menu/settings_button_on.png"),
            utils.load_image(
                f"{assets_path}/main_menu/settings_button_off.png"),
            utils.load_image(
                f"{assets_path}/main_menu/settings_button_clicked.png"),
            settings_button_action)
        self.quit_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/main_menu/quit_button_on.png"),
            utils.load_image(f"{assets_path}/main_menu/quit_button_off.png"),
            utils.load_image(f"{assets_path}/main_menu/quit_button_clicked.png"))

        padding = 10

        self.game_title.rect.centerx = self.screen_rect.centerx
        self.game_title.rect.top = self.screen_rect.top + padding

        self.play_button.rect.midleft = self.screen_rect.midleft
        self.play_button.rect.x += padding

        self.settings_button.rect.midleft = self.screen_rect.midleft
        self.settings_button.rect.y += 35 + padding
        self.settings_button.rect.x += padding

        self.quit_button.rect.midleft = self.screen_rect.midleft
        self.quit_button.rect.y += 80 + padding
        self.quit_button.rect.x += padding

    def draw(self):
        self.screen.fill((0, 0, 80))
        self.background.draw()
        self.draw_particles()
        self.game_title.draw()
        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()

    def update(self):
        self.background.update(self.particles_groups)
        self.update_particles()
        self.game_title.update()
        self.play_button.update()
        self.settings_button.update()
        self.quit_button.update()

    def update_on_event(self, event):
        self.play_button.update_on_event(event)
        self.settings_button.update_on_event(event)
        self.quit_button.update_on_event(event)


# TODO: Create settings scene. The projected interface file is settings_view.png
class SettingsScene(Scene):
    """Scene that displays the game setup."""

    def __init__(self, screen):
        super().__init__(screen)

        # Difficulty setting section
        self.difficulty_setting_label = interface.Label.from_text(
            screen, "DIFFICULTY", (170, 0, 0), 24, 10, 0, True,
            antialised=True
        )
        self.easy_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_settings/easy_button_on.png"),
            utils.load_image(f"{assets_path}/on_settings/easy_button_off.png"),
            utils.load_image(f"{assets_path}/on_settings/easy_button_clicked.png"))
        self.normal_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_settings/normal_button_on.png"),
            utils.load_image(
                f"{assets_path}/on_settings/normal_button_off.png"),
            utils.load_image(f"{assets_path}/on_settings/normal_button_clicked.png"))
        self.hard_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_settings/hard_button_on.png"),
            utils.load_image(f"{assets_path}/on_settings/hard_button_off.png"),
            utils.load_image(f"{assets_path}/on_settings/hard_button_clicked.png"))

        # Buttons setup
        for button in [self.easy_button, self.normal_button, self.hard_button]:
            button.rect.midtop = self.screen_rect.midtop
            button.rect.y += 20
        self.easy_button.rect.x -= 85
        self.hard_button.rect.x += 85

        # Back button
        def back_button_action():
            fadefx = transition.FadeTransition(
                self.screen, self.scene_manager, "main_menu", (255, 255, 255),
                4)
            self.scene_manager.change_scene("main_menu", fadefx)

        self.back_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_settings/back_button_on.png"),
            utils.load_image(f"{assets_path}/on_settings/back_button_off.png"),
            utils.load_image(
                f"{assets_path}/on_settings/back_button_clicked.png"),
            back_button_action
        )

        self.back_button.rect.bottomright = self.screen_rect.bottomright
        self.back_button.rect.x -= 15
        self.back_button.rect.y -= 15

        # Info section
        self.info_title_label = interface.Label.from_text(
            screen, "INFO:", (0, 0, 0), 28, 5, 0, True,
            antialised=True
        )
        info_string = "This project is not official. I made this just to " \
            + "practise my programming skills. One more thing that I have to " \
            + "improve in my projects are:"
        self.info_label = interface.Label.from_text(
            screen, info_string, (0, 0, 0), 26, 50, 1,
            antialised=True)
        to_be_improved_string = "° Design\n° Code efficiency" \
            + "\n° Avoid lazy code."
        self.to_be_improved_label = interface.Label.from_text(
            screen, to_be_improved_string, (0, 0, 0), 24, 25, 2,
            antialised=True)

        self.info_title_label.rect.midleft = self.screen_rect.midleft
        self.info_title_label.rect.x += 10
        self.info_label.rect.midleft = self.screen_rect.midleft
        self.info_label.rect.y += 50
        self.info_label.rect.x += 30
        self.to_be_improved_label.rect.topleft = self.info_label.rect.bottomleft
        self.to_be_improved_label.rect.y += 10
        self.to_be_improved_label.rect.x += 30

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.easy_button.draw()
        self.normal_button.draw()
        self.hard_button.draw()

        self.info_title_label.draw()
        self.info_label.draw()

        self.to_be_improved_label.draw()

        self.back_button.draw()

    def update(self):
        self.easy_button.update()
        self.normal_button.update()
        self.hard_button.update()

        self.back_button.update()

    def update_on_event(self, event):
        self.easy_button.update_on_event(event)
        self.normal_button.update_on_event(event)
        self.hard_button.update_on_event(event)
        self.back_button.update_on_event(event)


class GameScene(Scene):
    """Scene responsible for being actually the minigame."""

    def __init__(self, screen):
        super().__init__(screen)

        # Game flags
        self.paused = False
        self.game_over = False
        self.on_countdown = True

        # Timer variables
        self.current_time = 0
        self.countdown_tick = 0

        self.attempts = 3

        # Game elements
        self.ball = Ball(screen)
        self.paddle = Paddle(screen)
        self.targets = sprite.Group()
        target.recharge(screen, self.targets)

        # Interface elements
        self.background = ColourChangingBackground(screen)
        self.countdown_number = interface.Label.from_text(
            screen, "1", (0, 0, 255), 36, 1, 1)
        self.scoreboard = interface.Label.from_text(
            screen, f"Score: {self.ball.points}", (255, 255, 255), 16, 17, 1,
            True, antialised=True)
        self.game_over_label = interface.Label.from_text(
            screen, "GAME OVER", (255, 255, 255), 20, 10, 0, True,
            antialised=True)
        self.retry_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_game/retry_button_on.png"),
            utils.load_image(f"{assets_path}/on_game/retry_button_off.png"),
            utils.load_image(f"{assets_path}/on_game/retry_button_clicked.png"), self.retry)
        self.main_menu_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_game/main_menu_button_on.png"),
            utils.load_image(
                f"{assets_path}/on_game/main_menu_button_off.png"),
            utils.load_image(
                f"{assets_path}/on_game/main_menu_button_clicked.png"),
            lambda: self.scene_manager.change_scene(
                "main_menu",
                transition.FadeTransition(
                    screen, self.scene_manager, "main_menu",
                    (255, 255, 255), 4)
            )
        )
        self.paused_label = interface.Label.from_text(
            screen, "PAUSED", (100, 0, 0), 36, 6, 0, True, antialised=True)

        def back_button_action():
            fadefx = transition.FadeTransition(screen, self.scene_manager,
                                               "main_menu", (255, 255, 255), 4)
            self.scene_manager.change_scene("main_menu", fadefx)

            self.paused = False
            self.ball.points = 0

        self.back_button = interface.Button(
            screen, utils.load_image(
                f"{assets_path}/on_game/back_button_on.png"),
            utils.load_image(f"{assets_path}/on_game/back_button_off.png"),
            utils.load_image(f"{assets_path}/on_game/back_button_clicked.png"),
            back_button_action)

        # Sound effects
        self.game_over_soundfx = utils.load_soundfx(
            f"{assets_path}/on_game/soundfx/game_over.wav", volume=0.2)
        self.countdown_beep_soundfx = utils.load_soundfx(
            f"{assets_path}/on_game/soundfx/countdown_beep.wav", volume=0.2)

        self.setup_game_elements()
        self.setup_interface_elements()

    def setup_game_elements(self):
        self.ball.x, self.ball.y = self.screen_rect.center

        self.paddle.rect.centerx = self.screen_rect.centerx
        self.paddle.rect.centery = self.screen_rect.centery + 100

    def setup_interface_elements(self):
        self.paused_label.rect.center = self.screen_rect.center
        self.back_button.rect.midtop = self.paused_label.rect.midbottom
        self.back_button.rect.y += 20

        self.game_over_label.rect.center = self.screen_rect.center
        self.game_over_label.rect.y -= 20

        self.main_menu_button.rect.center = self.screen_rect.center
        self.main_menu_button.rect.x -= 50
        self.main_menu_button.rect.y += 30

        self.retry_button.rect.center = self.screen_rect.center
        self.retry_button.rect.x += 50
        self.retry_button.rect.y += 30

        self.countdown_number.rect.center = self.screen_rect.center

        self.scoreboard.rect.bottomright = self.screen_rect.bottomright

    def draw(self):
        if self.game_over:
            self.screen.fill((0, 20, 0))
            self.game_over_label.draw()
            self.main_menu_button.draw()
            self.retry_button.draw()
        else:
            # Game is on
            self.background.draw()
            self.targets.draw(self.screen)
            self.ball.draw()
            self.draw_particles()
            self.paddle.draw()
            self.scoreboard.draw()
            if self.paused:
                self.paused_label.draw()
                self.back_button.draw()
            elif self.on_countdown:
                self.countdown_number.draw()

    def update_game_elements(self):
        """It updates the game related elements."""

        if not (self.paused or self.on_countdown):
            if self.ball.rect.top > self.screen_rect.bottom:
                self.restart()
                self.attempts -= 1
                if self.attempts == 0:
                    self.game_over = True
                    self.on_countdown = False
                    self.game_over_soundfx.play()
            self.background.update()
            self.ball.update(self.particles_groups, self.paddle)
            self.update_particles()
            self.paddle.update()
            self.targets.update(self.ball, self.particles_groups)
            self.scoreboard.update_text(f"Score: {self.ball.points}")
            self.scoreboard.rect.bottomleft = self.screen_rect.bottomleft
        else:
            self.back_button.update()

        if self.game_over:
            self.retry_button.update()
            self.main_menu_button.update()

    def countdown_handling(self):
        """It's responsible for doing the game 1.. 2.. 3.. countdown
        whenever asked to do so.
        """

        if not (self.countdown_tick or self.game_over) and self.on_countdown:
            self.countdown_tick = time.get_ticks()

            # The beep sound effect is just a sec. Better that way.
            self.countdown_beep_soundfx.play(loops=2)

        if self.on_countdown:
            delta_time = self.current_time - self.countdown_tick

            for i in range(1, 4):
                if i*1000-1000 < delta_time < i*1000:
                    self.countdown_number.update_text(str(i))
                    self.countdown_number.rect.center = self.screen_rect.center
            else:
                if 3000 < delta_time < 3500:
                    self.on_countdown = False
                    self.countdown_tick = 0

    def update(self):
        self.current_time = time.get_ticks()

        self.countdown_handling()
        self.update_game_elements()

    def update_on_event(self, event):
        if event.type == constants.KEYDOWN:
            if event.key == constants.K_a:
                self.paddle.move_left(True)
            elif event.key == constants.K_d:
                self.paddle.move_right(True)
            elif event.key == constants.K_p and not self.on_countdown:
                self.paused = not self.paused
        elif event.type == constants.KEYUP:
            if event.key == constants.K_a:
                self.paddle.move_left(False)
            elif event.key == constants.K_d:
                self.paddle.move_right(False)

        if self.game_over:
            self.retry_button.update_on_event(event)
            self.main_menu_button.update_on_event(event)
        elif self.paused:
            self.back_button.update_on_event(event)

    def restart(self):
        """It restarts the game to its initial state."""

        target.recharge(self.screen, self.targets)
        self.setup_game_elements()
        self.countdown_tick = 0
        self.on_countdown = True

    def retry(self):
        """It starts the game again."""

        self.restart()
        self.attempts = 3
        self.countdown_tick = 0
        self.on_countdown = True
        self.game_over = False
