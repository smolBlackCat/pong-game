"""Module that provides some widgets and functions to deal with the
game interface.
"""

import textwrap

import pygame


class Button(pygame.sprite.Sprite):
    """This class represents a interface button on a game. The button can have
    any look, as it has the off and on variants.
    """

    def __init__(self, screen, button_on_image, button_off_image,
                 button_clicked_image, action=None):
        """Initialises the Button object.

        Args:
            screen:
                A pygame Surface object that represents the screen.

            button_on_image:
                The loaded sprite of the button when the mouse is
                above the button.

            button_off_image:
                The loaded sprite of the button when the mouse is not
                above the button.
            
            button_clicked_image:
                The loaded sprite of the button when the mouse clicks
                the button.
            
            action:
                A function that is always executed when the button is
                pressed.
        """

        self.screen = screen
        self.button_on_image = button_on_image
        self.button_off_image = button_off_image
        self.button_clicked_image = button_clicked_image
        self.current_sprite = button_off_image
        self.rect = self.current_sprite.get_rect()
        self.action = action

    def draw(self):
        """Draws the button on the screen."""

        self.screen.blit(self.current_sprite, self.rect)

    def update(self, event):
        """Updates the button according to the user actions.
        
        User actions == Hover the mouse on the button, Click the
        button and etc.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_sprite = self.button_on_image
            if pygame.mouse.get_pressed()[0]:
                self.current_sprite = self.button_clicked_image
        else:
            self.current_sprite = self.button_off_image
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.current_sprite = self.button_off_image
                if self.action is not None:
                    self.action()


class Label(pygame.sprite.Sprite):
    """Class that represents a label on a game."""

    def __init__(self, screen, image, animation=None, *animation_args):
        """Initialises the Label object.

        Args:
            screen:
                A Surface object representing the game window.
            
            image:
                May be a loaded image or a generated by pygame, like
                texts.

            animation:
                A function that executes the animation, like a
                floating object.
        """

        self.screen = screen
        self.image = image
        self.animation = animation
        self.animation_args = list(animation_args)
        self.rect = image.get_rect()

        self.yspeed = 3

    def draw(self):
        """Draws the label on the screen."""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updates the label on the screen."""

        if self.animation is not None:
            args = [self] + self.animation_args
            self.animation(*args)


    @staticmethod
    def from_text(screen, text, colour, size, chars_per_line, y_padding, 
                  bold=False, italic=False, antialised=False):
        """Creates a label object based on a text.

        Args:
        
            screen:
                Surface object representing the screen.

            text:
                str object containing the text to be generated for
                this label.

            size:
                The character size.

            chars_per_line:
                the amount of characters in each line.

            bold:
                Optional arg where determines if the text is bold or
                not.

            italic:
                Optional arg where determines if the text is italic
                or not.
        """

        font = pygame.font.SysFont(None, size, bold, italic)
        rendered_paragraph = [
            font.render(phrase, antialised, colour)
            for phrase in textwrap.wrap(text, chars_per_line)
        ]

        height = sum(
            [phrase.get_height() + y_padding for phrase in rendered_paragraph]
        )
        width = max([phrase.get_width() for phrase in rendered_paragraph])
        text_bg = pygame.Surface((width, height), pygame.SRCALPHA)

        row = 0
        for phrase in rendered_paragraph:
            rect = phrase.get_rect()
            rect.y = row
            text_bg.blit(phrase, rect)
            row += font.get_height() + y_padding
        
        return Label(screen, text_bg)


    @staticmethod
    def from_image(screen, image, animation=None, *animation_args):
        """Creates a Label object based on a image.

        Args:

            screen:
                Surface object representing the screen.

            image:
                Surface object made from a loaded sprite.

            animation:
                Function that executes a kind of animation.

            animation_args:
                In this arg you'll put a set of arguments needed to
                the animation function work.

        Returns:

            A Label object made from a loaded sprite.
        """

        return Label(screen, image, animation, *animation_args)