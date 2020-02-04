from abc import abstractmethod, ABC

from pygame import Surface, Rect, Vector2
from pygame.sprite import Sprite

from constants import PHYSICS_SCALE


class Moveable(ABC):

    @abstractmethod
    def move(self, of: Vector2, physics_scale=False):
        pass


class GameObject(Sprite, Moveable):

    def __init__(self, surface: Surface):
        Sprite.__init__(self)
        self.image: Surface = surface.convert()

        self._rect: Rect = self.image.get_rect()
        self._rect_dirty = False
        self.transform = Vector2(self._rect.x, self._rect.y)

    @property
    def rect(self) -> Rect:
        # Caching
        if self._rect_dirty:
            self._rect = self.image.get_rect().move(int(self.transform.x), int(self.transform.y))
            self._rect_dirty = False

        return self._rect

    @property
    def height(self) -> int:
        return self.image.get_height()

    @property
    def width(self) -> int:
        return self.image.get_width()

    @property
    def center(self) -> Vector2:
        return self.transform + Vector2(self.width, self.height)

    def move(self, of: Vector2, physics_scale=False):
        # Invalidate rect
        self._rect_dirty = True

        if physics_scale:
            self.transform += of / PHYSICS_SCALE
        else:
            self.transform += of

    # Provide the generic signature
    # To be overridden
    def update(self, delta_time: float):
        pass
