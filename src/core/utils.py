"""Utilities functions and classes modules."""

import functools
import os

import pygame.image as image
import pygame.mixer as mixer
import pygame.surface as surface


def load_image(path: str) -> surface.Surface:
    """Loads a image file into a pygame.surface.Surface object.

    Args:

        path: Image location. It can be absolute or relative.

    Returns:
        The image built upon a pygame.surface.Surface object.
    """

    return image.load(os.path.join(path))


@functools.cache
def load_soundfx(path: str, volume: float = 1.0) -> mixer.Sound:
    """Loads a sound effect.

    Args:

        path: Sound effect location. It can be absolute or relative.
    """

    sound_fx = mixer.Sound(os.path.join(path))
    sound_fx.set_volume(volume)
    return sound_fx
