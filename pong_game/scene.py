import pygame.constants as constants
import pygame.draw as draw
import pygame.rect as rect
import pygame.surface as surface
import pygame.time as time

from . import effects, interface, utils
from .game_elements.ball import Ball
from .game_elements.paddle import Paddle
from .game_elements.targets import Targets

# TODO: Create a settings view


class Scene:
    """A base object for the creation of scenes in a screen."""

    def __init__(self, screen):
        """Initialises the Scene object.

        Args:

            screen:
                The Surface object where this scene will be drawn.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # This variable is only filled when this scene is added to a
        # scene manager instance.
        self.scene_manager = None

    def draw(self):
        """It draws the components of this scene in the screen."""

        pass

    def update(self):
        """It updates the components everytime in the loop."""

        pass

    def update_on_event(self, event):
        """It updates the components if a event occur.
        
        Args:
        
            event:
                This is an object passed by the iteration, that is
                responsible for iterating all events
                (pygame.event.get()).
        """

        pass


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
        self.test_rect = rect.Rect(0, 0, 75, 30)
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
            screen, utils.load_image("game_intro/moura_cat.png"))
        self.logo_title = interface.Label(
            screen, utils.load_image("game_intro/logo_title.png"))

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
            self.scene_manager.change_view(
                "main_menu",
                effects.FadeTransition(
                    self.screen, self.scene_manager, "main_menu",
                    (0, 0, 0), 4))


class MainMenuScene(Scene):
    """A scene that shows the "game" main menu."""

    def __init__(self, screen):
        super().__init__(screen)

        self.game_title = interface.Label(
            screen, utils.load_image("main_menu/game_title.png"),
            effects.floating_animation, 120, self.screen_rect.top)

        def play_button_action():
            fadefx = effects.FadeTransition(
                self.screen, self.scene_manager, "on_game", (255, 255, 0))
            self.scene_manager.change_view(
                "on_game", fadefx)

            # Always get brand new game
            self.scene_manager.views["on_game"].retry()

        self.play_button = interface.Button(
            screen, utils.load_image("main_menu/play_button_on.png"),
            utils.load_image("main_menu/play_button_off.png"),
            utils.load_image("main_menu/play_button_clicked.png"),
            play_button_action)

        def settings_button_action():
            pass

        self.settings_button = interface.Button(
            screen, utils.load_image("main_menu/settings_button_on.png"),
            utils.load_image("main_menu/settings_button_off.png"),
            utils.load_image("main_menu/settings_button_clicked.png"),
            settings_button_action)
        self.quit_button = interface.Button(
            screen, utils.load_image("main_menu/quit_button_on.png"),
            utils.load_image("main_menu/quit_button_off.png"),
            utils.load_image("main_menu/quit_button_clicked.png"))

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
        self.game_title.draw()
        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()

    def update(self):
        self.game_title.update()
        self.play_button.update()
        self.settings_button.update()
        self.quit_button.update()

    def update_on_event(self, event):
        self.play_button.update_on_event(event)
        self.settings_button.update_on_event(event)
        self.quit_button.update_on_event(event)


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
        self.targets = Targets(screen)

        # Interface elements
        self.countdown_number = interface.Label.from_text(
            screen, "1", (0, 0, 255), 36, 1, 1)
        self.scoreboard = interface.Label.from_text(
            screen, f"Score: {self.ball.points}", (255, 255, 255), 16, 17, 1,
            True, antialised=True)
        self.game_over_label = interface.Label.from_text(
                screen, "GAME OVER", (255, 255, 255), 20, 10, 0, True,
                antialised=True)
        self.retry_button = interface.Button(
            screen, utils.load_image("on_game/retry_button_on.png"),
            utils.load_image("on_game/retry_button_off.png"),
            utils.load_image("on_game/retry_button_clicked.png"), self.retry)
        self.main_menu_button = interface.Button(
            screen, utils.load_image("on_game/main_menu_button_on.png"),
            utils.load_image("on_game/main_menu_button_off.png"),
            utils.load_image("on_game/main_menu_button_clicked.png"),
            lambda: self.scene_manager.change_view(
                "main_menu",
                effects.FadeTransition(
                    screen, self.scene_manager, "main_menu",
                    (255, 255, 255), 4)
            )
        )
        self.paused_label = interface.Label.from_text(
            screen, "PAUSED", (100, 0, 0), 36, 6, 0, True, antialised=True)

        # Sound effects
        self.game_over_soundfx = utils.load_soundfx(
            "on_game/soundfx/game_over.wav")
        self.countdown_beep_soundfx = utils.load_soundfx(
            "on_game/soundfx/countdown_beep.wav")

        self.setup_game_elements()
        self.setup_interface_elements()

    def setup_game_elements(self):
        self.ball.x, self.ball.y = self.screen_rect.center

        self.paddle.rect.centerx = self.screen_rect.centerx
        self.paddle.rect.centery = self.screen_rect.centery + 100

    def setup_interface_elements(self):
        self.paused_label.rect.center = self.screen_rect.center

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
            self.screen.fill((0, 0, 20))
            self.targets.draw()
            self.ball.draw()
            self.paddle.draw()
            self.scoreboard.draw()
            if self.paused:
                self.paused_label.draw()
            elif self.on_countdown:
                self.countdown_number.draw()

    def update_game_elements(self):
        """It updates the game related elements."""

        if not (self.paused or self.on_countdown):
            self.ball.update(self.paddle)
            if self.ball.rect.top > self.screen_rect.bottom:
                self.restart()
                self.attempts -= 1
                if self.attempts == 0:
                    self.game_over = True
                    self.on_countdown = False
                    self.game_over_soundfx.play()
            self.paddle.update()
            self.targets.update(self.ball)
            self.scoreboard.update_text(f"Score: {self.ball.points}")
            self.scoreboard.rect.bottomleft = self.screen_rect.bottomleft

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

    def restart(self):
        """It restarts the game to its initial state."""

        self.targets.recharge()
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


class SceneManager:
    """Manages the scenes in the main thread of the running game."""

    def __init__(self):
        """Initialises the scene manager object."""

        self.views = dict()
        self.on_transition = False
        self.fx_object = None
        self.current_view = None

    def add(self, view_name, scene_object):
        """Adds a view to the scene manager.

        Args:

            view_name:
                A name to the view. It will be used for example when
                a scene change is requested.

            scene_object:
                A object that contains all the components to be drawn
                on the screen.
        """

        scene_object.scene_manager = self
        self.views[view_name] = scene_object

    def show(self):
        """Shows the current view. This function may not have only
        one behavior
        """

        self.views[self.current_view].draw()
        if self.on_transition:
            self.fx_object.animate()

    def update(self):
        """It updates the components of the current scene in loop."""

        if not self.on_transition:
            self.views[self.current_view].update()

    def update_on_event(self, event):
        """It updates scenes based on events being read by the for
        loop.

        Args:

            event:
                A pygame Event object. This args is the event in the
                for loop, that is responsible for reading each
                event.
        """

        if not self.on_transition:
            self.views[self.current_view].update_on_event(event)

    def _change_view(self, view_name):
        """It changes the current view directly."""

        self.current_view = view_name

    def change_view(self, view_name, fx=None):
        """It changes the current scene with a special effect or
        not.

        Args:

            view_name:
                The codename of the view to be the new current_view.

            fx:
                A class that is responsible for a transition of
                views. When none, the view is changed abruptly
        """

        if view_name != self.current_view:
            if fx is not None:
                self.fx_object = fx
                self.on_transition = True
            else:
                # Changes the view abruptly.
                self._change_view(view_name)

    def initial_view(self, view_name):
        """Sets the initial view for the scene manager."""

        self.current_view = view_name
