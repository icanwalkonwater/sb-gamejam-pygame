from pygame import Surface
from pygame import font as pyfont
from pygame.constants import SRCALPHA

from constants import GlobalSettings
from game_objects.game_object import GameObject
from ui.information_banner import InformationBanner


class DeathScreen(GameObject):
    def __init__(self, content=None):
        death_screen_background_surface = Surface((1024, 768), flags=SRCALPHA)
        death_screen_background_surface.fill((50, 50, 50, 100))

        font = pyfont.Font(GlobalSettings.FONT, 33)
        text_surface: Surface = InformationBanner.render_font(font, "Vous êtes Mort".upper())
        death_screen_background_surface.blit(text_surface,
                                             InformationBanner.title_text_placer(death_screen_background_surface,
                                                                                 text_surface))

        font = pyfont.Font(GlobalSettings.FONT, 19)
        text_surface: Surface = InformationBanner.render_font(font, "Le village de Vonorof été anéanti".upper())
        death_screen_background_surface.blit(text_surface,
                                             InformationBanner.content_text_placer(death_screen_background_surface,
                                                                                   text_surface))

        GameObject.__init__(self, death_screen_background_surface)

    def start(self, scene):
        scene.ui.empty()
        scene.ui.add(self)

    @staticmethod
    def content_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() - text.get_height() * 2.5

    @staticmethod
    def title_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() / 2 - text.get_height()
