import pygame

from .game_elements.ball import Ball

from .game_elements.paddle import Paddle

from . import effects, interface, utils


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
        """It updates the components if a event occur."""
        pass


class DebugScene(Scene):
    """Simple scene class that displays a white background. Mainly
    used to debug new stuff.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill((200, 200, 200))

        self.rect = self.bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Do whatever you want here
        self.ball = Ball(screen)
        self.ball.pos = [300, 200]

    def draw(self):
        self.screen.blit(self.bg, self.rect)
        self.ball.draw()

    def update_on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.ball.pos[1] -= 100
            elif event.key == pygame.K_DOWN:
                self.ball.pos[1] += 100


class IntroScene(Scene):
    """A scene that shows the logo of the creator of the game."""

    END_INTRO = pygame.USEREVENT + 1

    def __init__(self, screen):
        super().__init__(screen)

        self.logo_icon = interface.Label.from_image(
            screen, utils.load_image("game_intro/moura_cat.png"))
        self.logo_title = interface.Label.from_image(
            screen, utils.load_image("game_intro/logo_title.png"))

        self.logo_icon.rect.centerx = self.screen_rect.centerx
        self.logo_icon.rect.centery = self.screen_rect.centery
        self.logo_title.rect.centerx = self.screen_rect.centerx
        self.logo_title.rect.centery = self.screen_rect.centery + 74

        pygame.time.set_timer(IntroScene.END_INTRO, 3000, 1)

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

        def play_button_action(): return self.scene_manager.change_view(
            "on_game",
            effects.FadeTransition(
                self.screen, self.scene_manager, "on_game", (255, 255, 0)))
        self.play_button = interface.Button(
            screen, utils.load_image("main_menu/play_button_on.png"),
            utils.load_image("main_menu/play_button_off.png"),
            utils.load_image("main_menu/play_button_clicked.png"),
            play_button_action)
        self.settings_button = interface.Button(
            screen, utils.load_image("main_menu/settings_button_on.png"),
            utils.load_image("main_menu/settings_button_off.png"),
            utils.load_image("main_menu/settings_button_clicked.png"))
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

    def update_on_event(self, event):
        self.play_button.update(event)
        self.settings_button.update(event)
        self.quit_button.update(event)


class GameScene(Scene):
    """Shows the current game."""

    def __init__(self, screen):
        super().__init__(screen)

        self.ball = Ball(screen)
        self.paddle = Paddle(screen)

        self.ball.x, self.ball.y = self.screen_rect.center

        self.paddle.rect.centerx = self.screen_rect.centerx
        self.paddle.rect.centery = self.screen_rect.centery + 100

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.ball.draw()
        self.paddle.draw()
    
    def check_paddle_ball_collision(self):
        if self.paddle.rect.collidepoint(self.ball.x, self.ball.y):
            self.ball.yspeed *= -1

    def update(self):
        self.ball.update()
        self.paddle.update()
        self.check_paddle_ball_collision()

    def update_on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.paddle.move_left(True)
            elif event.key == pygame.K_RIGHT:
                self.paddle.move_right(True)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.paddle.move_left(False)
            elif event.key == pygame.K_RIGHT:
                self.paddle.move_right(False)


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
