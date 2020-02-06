import math

from pygame.color import Color
from pygame.rect import Rect

from constants import GlobalSettings, PlayerSettings
from entities.player import Player
from scene import Scene
from ui.progress_bar import UIProgressBar


class UIHealthBar(UIProgressBar):

    def __init__(self):
        top = GlobalSettings.RESOLUTION[1] - 30
        mid_screen = math.ceil(GlobalSettings.RESOLUTION[0] / 2)
        UIProgressBar.__init__(
            self, Rect((0, top), (mid_screen, 30)),
            color=Color(255, 0, 0), background_color=Color(255, 0, 0, 70),
            maximum=PlayerSettings.HEALTH_MAX, reverse=True
        )
        self.__player = None

    def start(self, scene: Scene):
        self.__player = scene.player.sprite

    def update(self, delta_time: float):
        self.value = self.__player.health
        UIProgressBar.update(self, delta_time)


class UIManaBar(UIProgressBar):

    def __init__(self):
        top = GlobalSettings.RESOLUTION[1] - 30
        mid_screen = math.floor(GlobalSettings.RESOLUTION[0] / 2)
        UIProgressBar.__init__(
            self, Rect((mid_screen, top), (mid_screen + 1, 30)),
            color=Color(0, 0, 255), background_color=Color(0, 0, 255, 70),
            maximum=PlayerSettings.MANA_MAX, value=PlayerSettings.MANA_MAX
        )
        self.__player = None

    def start(self, scene: Scene):
        self.__player = scene.player.sprite

    def update(self, delta_time: float):
        self.value = self.__player.mana
        UIProgressBar.update(self, delta_time)
