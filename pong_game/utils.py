"""Module dedicated for some utilities."""

import os

import pygame


def load_image(path):
    """Loads the image inside the game_data directory.

    Args:

        path:
            A string representing a path that comes after the root
            (game_data/)
    """

    return pygame.image.load(os.path.join("game_data", path))
