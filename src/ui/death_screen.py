import time

from pygame import Surface
from pygame import font as pyfont
from pygame.constants import SRCALPHA

from constants import GlobalSettings
from game_objects.game_object import GameObject
from scene_management import SceneManagement
from ui.information_banner import InformationBanner


class DeathScreen(GameObject):

    def __init__(self, text='YOU DIED', subtext='VONOROF\'S VILLAGE HAVE BEEN WIPED'):
        death_screen_background_surface = Surface((1024, 768), flags=SRCALPHA)
        death_screen_background_surface.fill((100, 100, 100, 200))

        font = pyfont.Font(GlobalSettings.FONT, 33)
        text_surface: Surface = DeathScreen.render_font(font, text)
        death_screen_background_surface.blit(text_surface,
                                             InformationBanner.title_text_placer(death_screen_background_surface,
                                                                                 text_surface))

        font = pyfont.Font(GlobalSettings.FONT, 19)
        text_surface: Surface = DeathScreen.render_font(font, subtext)
        death_screen_background_surface.blit(
            text_surface,
            InformationBanner.content_text_placer(
                death_screen_background_surface,
                text_surface
            )
        )

        GameObject.__init__(self, death_screen_background_surface)

        self.__reset_time = time.time() + 5

    def start(self, scene):
        scene.ui.empty()
        scene.ui.add(self)

    @staticmethod
    def render_font(font: pyfont.Font, string: str) -> Surface:
        return font.render(string, True, (255, 255, 255))

    def update(self, delta_time: float):
        if self.__reset_time <= time.time():
            SceneManagement.load_scene('main_menu')
        else:
            GameObject.update(self, delta_time)

    @staticmethod
    def content_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() - text.get_height() * 2.5

    @staticmethod
    def title_text_placer(banner: Surface, text: Surface) -> (int, int):
        return banner.get_width() / 2 - text.get_width() / 2, banner.get_height() / 2 - text.get_height()
