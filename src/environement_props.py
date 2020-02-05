from enum import Enum
from typing import Callable, Generator

from pygame import Vector2, Surface

from animation import AnimatedSprite
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject, ImpactSide, PhysicsReceiver
from player import Player


class WindGameObject(RigidPhysicsAwareGameObject):
    def __init__(self, surface: Surface, direction: Vector2, force: float):
        RigidPhysicsAwareGameObject.__init__(self, surface, 0)
        self.__direction = direction.normalize_ip()
        self.__force = force

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, PhysicsReceiver):
            other.apply_force(self.__direction * self.__force)


class ButtonState(Enum):
    ON = 1
    OFF = 2


class ButtonGameObject(RigidPhysicsAwareGameObject, AnimatedSprite):

    def __init__(self, surface: Surface, on_enter: [Callable[[], None]], on_stay_inside: [Callable[[], None]],
                 on_exit: [Callable[[], None]]):
        RigidPhysicsAwareGameObject.__init__(self, surface, 0)
        AnimatedSprite.__init__(self, {
            ButtonState.ON: ["button_on.png"],
            ButtonState.OFF: ["button_off.png"]
        }, 1, ButtonState.OFF)
        self.on_enter = on_enter
        self.on_enter.append(self.__hide)
        self.during_activation = on_stay_inside
        self.on_exit = on_exit
        self.on_exit.append(self.__show)
        self.is_enabled = False
        self.is_pressed = False

    def __show(self):
        self._state = ButtonState.OFF

    def __hide(self):
        self._state = ButtonState.ON

    def update(self, delta_time: float):
        self.is_pressed = False
        RigidPhysicsAwareGameObject.update(self, delta_time)
        AnimatedSprite.update(self, delta_time)
        if self.is_pressed != self.is_enabled:
            self.is_enabled = False

            for handler in self.on_exit:
                handler()

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, Player):
            self.is_pressed = True
            if not self.is_enabled:
                self.is_enabled = True
                for handler in self.on_enter:
                    handler()
            for handler in self.during_activation:
                handler()


class MovableCube(RigidPhysicsAwareGameObject):
    def __init__(self, surface: Surface, weight: float, force_threshold: float):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight)
        self.force_threshold = force_threshold

    def apply_force(self, force: Vector2):
        if force.magnitude > self.force_threshold:
            RigidPhysicsAwareGameObject.apply_force(self, force)


class PathFollowingGameObject(GameObject):
    def __init__(self, surface: Surface, path_creator: Callable[[], Generator], start_on_creation: bool = True):
        GameObject.__init__(self, surface)
        self.__path_creator = path_creator
        self.__path_generator = None
        if start_on_creation:
            self.start()

    def update(self, delta_time: float):
        if self.path_generator:
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
