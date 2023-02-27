"""Module for in-game transitions."""

import pygame.surface as surface


class Transition:
    """Base transition class.

    Transition works in pair with SceneManager as Transition is the
    one that actually changes from a scene to another but animated.
    """

    def __init__(self, screen: surface.Surface, scene_manager, next_scene):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.scene_manager = scene_manager
        self.next_view = next_scene

    def animate(self) -> None:
        pass

    def clean(self) -> None:
        """Always called in the end of the animate method."""

        self.scene_manager.on_transition = False
        self.fx_object = None


class FadeTransition(Transition):
    """Fade-in and Fade-out Transition."""

    def __init__(self, screen, scene_manager, next_view, fade_colour,
                 speed_factor=2):
        super().__init__(screen, scene_manager, next_view)

        # Fade elements
        self.fade_bg = surface.Surface(screen.get_size())
        self.fade_bg.set_alpha(0)
        self.fade_bg.fill(fade_colour)
        self.rect = self.fade_bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Fade params
        self.on_fade = True
        self.alpha = 0
        self.factor = speed_factor
        self.backwards = False
        self.c = 0

    def animate(self) -> None:
        """It fades the screen to the next view."""

        if self.on_fade:
            if self.c == 1:
                # The scene is covered. Change the scene
                self.scene_manager.change_scene(self.next_view)

            self.alpha += self.factor
            if (self.alpha > 255 and not self.backwards) \
                    or (self.alpha < 0 and self.backwards):
                self.backwards = not self.backwards
                self.factor *= -1
                self.c += 1

            self.fade_bg.set_alpha(self.alpha)
            self.screen.blit(self.fade_bg, self.rect)

            if self.c == 2:
                self.on_fade = False
        else:
            self.clean()
