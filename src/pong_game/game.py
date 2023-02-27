"""Pong game main function."""

import pygame

from core import game

from . import scene as pong_scenes


class PongGame(game.Game):
    """Game child that displays a simple pong game."""

    def __init__(self, screen_width: int, screen_height: int, name: str, icon: pygame.Surface = None):
        super().__init__(screen_width, screen_height, name, icon)
    
    def setup_scenes(self) -> None:
        intro_scene = pong_scenes.IntroScene(self.screen)
        main_menu_scene = pong_scenes.MainMenuScene(self.screen)
        settings_scene = pong_scenes.SettingsScene(self.screen)
        game_scene = pong_scenes.GameScene(self.screen)
        debug_scene = pong_scenes.DebugScene(self.screen)
        self.scene_manager.add("game_intro", intro_scene)
        self.scene_manager.add("main_menu", main_menu_scene)
        self.scene_manager.add("on_settings", settings_scene)
        self.scene_manager.add("on_game", game_scene)
        self.scene_manager.add("debug", debug_scene)
        self.scene_manager.initial_view("game_intro")
