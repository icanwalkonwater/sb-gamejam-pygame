from typing import List

from pygame import Surface, Rect
from pygame.sprite import Group, RenderUpdates, GroupSingle

from constants import Layers
from game_object import GameObject


class Scene:

    def __init__(self, background: Surface, statics: List[GameObject], dynamics: List[GameObject]):
        self.background: Surface = background
        # Cached background with every statics blighted on it
        self.__background: Surface = None
        self.statics: Group = Group(statics)
        self.dynamics: RenderUpdates = RenderUpdates(dynamics)
        self.layers = {
            Layers.ENVIRONMENT: Group(),
            Layers.PLAYER: GroupSingle(),
            Layers.ENEMY: Group(),
            Layers.PROJECTILE: Group()
        }

    @property
    def environment(self) -> Group:
        return self.layers[Layers.ENVIRONMENT]

    @property
    def player(self) -> GroupSingle:
        return self.layers[Layers.PLAYER]

    @property
    def enemies(self) -> Group:
        return self.layers[Layers.ENEMY]

    @property
    def projectiles(self) -> Group:
        return self.layers[Layers.PROJECTILE]

    def draw_init(self, surface: Surface):
        # Reset background
        self.__background: Surface = self.background.copy()
        # Blit statics onto background
        self.__background.blits(
            ((go.image, go.rect) for go in self.statics.sprites())
        )

        surface.blit(self.__background, (0, 0))

    def draw_auto(self, surface: Surface):
        # Clear the dynamic objects
        self.dynamics.clear(surface, self.__background)

        # Redraw the dynamics and return the invalidated areas
        return self.dynamics.draw(surface)

    def draw_statics(self, surface: Surface):
        surface.blit(self.background, (0, 0))
        self.statics.draw(surface)

    def draw_dynamics(self, surface: Surface) -> List[Rect]:
        self.dynamics.clear(surface, self.background)
        return self.dynamics.draw(surface)

    def update(self, delta_time: float):
        self.statics.update(delta_time)
        self.dynamics.update(delta_time)
