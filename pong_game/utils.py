"""Module dedicated for some utilities."""

import os

import pygame.image as image
import pygame.mixer as mixer

def load_image(path):
    """Loads the image inside the game_data directory.

    Args:

        path:
            A string representing a path that comes after the root
            (game_data/)
    """

    return image.load(os.path.join("game_data", path))


def load_soundfx(path):
    """Loads the soundfx inside the soundfx directory, a subdirectory
    of game_data.
    
    Args:
    
        path:
            A string representing a path that comes after the root
            (game_data/)
    """

    return mixer.Sound(os.path.join("game_data", path))
