import time
from ast import Str

from pygame import font as pyfont, Surface
from pygame.constants import SRCALPHA
from pygame import Vector2

from constants import GlobalSettings
from game_objects.game_object import GameObject


class Vecteur2(object):
    pass


class InformationBanner(GameObject):
    def __init__(self, title: Str, content: Str, duration: float):
        banner_background_surface = Surface((1024, 150), flags=SRCALPHA)
        banner_background_surface.fill((111, 111, 111, 200))

        font = pyfont.Font(GlobalSettings.FONT, 33)
        text_surface: Surface = InformationBanner.render_font(font, title.upper())
        banner_background_surface.blit(text_surface,
                                       InformationBanner.title_text_placer(banner_background_surface, text_surface))

        font = pyfont.Font(GlobalSettings.FONT, 19)
        text_surface: Surface = InformationBanner.render_font(font, content.upper())
        banner_background_surface.blit(text_surface,
                                       InformationBanner.content_text_placer(banner_background_surface, text_surface))

        GameObject.__init__(self, banner_background_surface)

        self._duration = duration
        self._death_time = 0

    def start(self, scene):
        scene.ui.add(self)
        self.move(Vector2(0, 500))
        self._death_time = time.time() + self._duration

    @staticmethod
    def render_font(font: pyfont.Font, string: Str) -> Surface:
        return font.render(string, True, (255, 255, 255))

    @staticmethod
    def content_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() - text.get_height() * 2.5

    @staticmethod
    def title_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() / 2 - text.get_height()

    def update(self, delta_time: float):
        if time.time() > self._death_time:
            self.kill()
        GameObject.update(self, delta_time)
