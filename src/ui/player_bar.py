from pygame.color import Color
from pygame.rect import Rect

from constants import PlayerSettings
from scene import Scene
from ui.progress_bar import UIProgressBar


class UIHealthBar(UIProgressBar):

    def __init__(self):
        UIProgressBar.__init__(
            # Pixel perfect position from the overlay
            self, Rect((28, 49), (201, 18)),
            color=Color(255, 0, 0), background_color=Color(255, 0, 0, 70),
            maximum=PlayerSettings.HEALTH_MAX
        )
        self.__player = None

    def start(self, scene: Scene):
        self.__player = scene.player.sprite

    def update(self, delta_time: float):
        self.value = self.__player.health
        UIProgressBar.update(self, delta_time)


class UIManaBar(UIProgressBar):

    def __init__(self):
        UIProgressBar.__init__(
            # Pixel perfect position from the overlay
            self, Rect((28, 110), (201, 18)),
            color=Color(0, 0, 255), background_color=Color(0, 0, 255, 70),
            maximum=PlayerSettings.MANA_MAX, value=PlayerSettings.MANA_MAX
        )
        self.__player = None

    def start(self, scene: Scene):
        self.__player = scene.player.sprite

    def update(self, delta_time: float):
        self.value = self.__player.mana
        UIProgressBar.update(self, delta_time)
