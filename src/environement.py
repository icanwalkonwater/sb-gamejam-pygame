from wsgiref.handlers import format_date_time

from pygame import Vector2, Surface
from typing import Callable, Generator

from game_object import GameObject
from player import Player
from physics import RigidPhysicsAwareGameObject, ImpactSide, PhysicsReceiver


class WindGameObject(RigidPhysicsAwareGameObject):
    def __init__(self, surface: Surface, direction: Vector2, force: float):
        super().__init__(surface, 0)
        self.direction = direction
        self.force = force

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, PhysicsReceiver):
            other.apply_force(self.direction.normalize() * self.force)

class ButtonGameObject(RigidPhysicsAwareGameObject):
    def __show(self):
        self.image.fill((127, 127, 127, 255))

    def __hide(self):
        self.image.fill((0, 0, 0, 0))

    def __init__(self, surface: Surface, on_enter: [Callable[[], None]], during_activation: [Callable[[], None]],
                 on_exit: [Callable[[], None]]):
        super().__init__(surface, 0)
        self.on_enter = on_enter
        self.on_enter.append(self.__hide)
        self.during_activation = during_activation
        self.on_exit = on_exit
        self.on_exit.append(self.__show)
        self.is_on = False
        self.is_pressed = False

    def update(self, delta_time: float):
        self.is_pressed = False
        super().update(delta_time)
        if self.is_pressed != self.is_on:
            self.is_on = False

            for handler in self.on_exit:
                handler()

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, Player):
            self.is_pressed = True
            if not self.is_on:
                self.is_on = True
                for handler in self.on_enter:
                    handler()
            for handler in self.during_activation:
                handler()

class PushableCube(RigidPhysicsAwareGameObject):
    def __init__(self, surface: Surface, weight: float, force_threashold : float):
        super().__init__(surface, weight)
        self.force_threashold  = force_threashold

    def apply_force(self, force: Vector2):
        if force.magnitude>self.force_threashold:
            super().apply_force(force)

class PathFollowingGameObject(GameObject):
    def __init__(self, surface: Surface, path_creator: Callable[[], Generator], start_on_creation : bool = True):
        super().__init__(surface)
        self.path_creator = path_creator
        self.path_generator = None
        if start_on_creation :
            self.start()


    def update(self, delta_time: float):
        if self.path_generator :
            try:
                new_pos = next(self.path_generator)
            except StopIteration:
                new_pos = None
            if new_pos:
                self._rect_dirty = True
                self.transform = new_pos
            else:
                self.path_generator = None

    def start(self):
        self.path_generator = self.path_creator()

    def stop(self):
        self.path_generator = None

