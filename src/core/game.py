"""Base Game class."""

import pygame

from . import scene


class Game:
    """Base class for implementing specific game instances."""

    def __init__(self, screen_width: int, screen_height: int, name: str,
                 icon: pygame.Surface = None):
        pygame.init()
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__name = name

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(name)
        if icon is not None:
            pygame.display.set_icon(icon)
        self.scene_manager = scene.SceneManager()
        self.clock = pygame.time.Clock()
        self.setup_scenes()

    def setup_scenes(self) -> None:
        """Sets up the scenes of the game. This method is the method
        to be overloaded by children classes implementing this class.
        """

        pass

    def start(self) -> None:
        """Main loop of the game."""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.scene_manager.update_on_event(event)

            self.scene_manager.show()
            self.scene_manager.update()

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def width(self) -> int:
        return self.__screen_width

    @property
    def height(self) -> int:
        return self.__screen_height
