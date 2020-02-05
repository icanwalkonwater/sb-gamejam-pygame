from pygame.color import Color
from pygame.constants import SRCALPHA
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from game_object import GameObject


class UIProgressBar(GameObject):
    TRANSPARENT = Color(0, 0, 0, 0)

    def __init__(self, area: Rect, color: Color, maximum: float = 1, value: float = 0):
        surface: Surface = Surface((area.width, area.height), flags=SRCALPHA)
        surface.fill(color)
        GameObject.__init__(self, surface)
        self._area = area
        self._color: Color = color
        self._max: float = maximum
        self.__percent: float
        self.__dirty: bool = True
        self.value = value

        self.move(Vector2(area.x, area.y))

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = max(0, min(self._max, value))
        self.__percent = value / self._max
        self.__dirty = True

    def __update_sprite(self):
        if self.__dirty:
            fill_rect: Rect = self._area.move(-self._area.width * (1 - self.__percent), 0).clip(self._area)
            fill_rect.top = 0
            dry_rect: Rect = self._area.move(self._area.width * self.__percent, 0).clip(self._area)
            dry_rect.top = 0

            self.image.fill(self._color, fill_rect)
            self.image.fill(Color(255, 255, 255), dry_rect)

            self.__dirty = False

    def update(self, delta_time: float):
        self.value -= .0001 * delta_time
        self.__update_sprite()
        GameObject.update(self, delta_time)
