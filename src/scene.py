from typing import List

from pygame import Surface, Rect
from pygame.sprite import Group, RenderUpdates

from game_object import GameObject


class Scene:

    def __init__(self, background: Surface, statics: List[GameObject], dynamics: List[GameObject]):
        self.background: Surface = background
        self.statics: Group = Group(statics)
        self.dynamics: RenderUpdates = RenderUpdates(dynamics)

    def draw_init(self, surface: Surface):
        surface.blit(self.background, (0, 0))

    def draw_auto(self, surface: Surface):
        # Clear the dynamic objects
        self.dynamics.clear(surface, self.background)
        # Redraw the statics (in case there was a dynamics on top of them)
        self.statics.draw(surface)

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
