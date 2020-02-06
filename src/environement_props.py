from typing import Callable, Generator

from pygame import Vector2, Surface

from animation import AnimatedSprite
from entities.player import Player
from enums import ImpactSide, ButtonState
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject, PhysicsReceiver
from ressource_management import ResourceManagement
from scene import Scene


class WindGameObject(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, direction: Vector2, force: float):
        RigidPhysicsAwareGameObject.__init__(self, surface, 0)
        self.__direction = direction.normalize()
        self.__force = force

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, PhysicsReceiver):
            other.apply_force(self.__direction * self.__force * delta_time)


class ButtonGameObject(RigidPhysicsAwareGameObject, AnimatedSprite):

    def __init__(self, on_enter: [Callable[[], None]] = None, on_stay_inside: [Callable[[], None]] = None,
                 on_exit: [Callable[[], None]] = None):
        sprites = ResourceManagement.get_environment_button_sprites()
        first_sprite = next(iter(sprites.values()))[0]

        RigidPhysicsAwareGameObject.__init__(self, first_sprite, 0)
        AnimatedSprite.__init__(self, sprites, 1, ButtonState.OFF)
        self.on_enter = on_enter if on_enter is not None else []
        self.on_enter.append(self.__hide)

        self.during_activation = on_stay_inside if on_stay_inside is not None else []

        self.on_exit = on_exit if on_exit is not None else []
        self.on_exit.append(self.__show)

        self.was_pressed = False
        self.is_pressed = False

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def __show(self):
        self._state = ButtonState.OFF

    def __hide(self):
        self._state = ButtonState.ON

    def update(self, delta_time: float):
        self.is_pressed = False
        RigidPhysicsAwareGameObject.update(self, delta_time)
        AnimatedSprite.update(self, delta_time)
        if self.is_pressed != self.was_pressed:
            self.was_pressed = False

            for handler in self.on_exit:
                handler()

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, Player):
            self.is_pressed = True
            if not self.was_pressed:
                self.was_pressed = True
                [handler() for handler in self.on_enter]
            [handler() for handler in self.during_activation]


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
        if self.__path_generator:
            try:
                new_pos = next(self.__path_generator)
            except StopIteration:
                new_pos = None
            if new_pos:
                self._rect_dirty = True
                self.transform = new_pos
            else:
                self.__path_generator = None

    def start(self):
        self.__path_generator = self.__path_creator()

    def stop(self):
        self.__path_generator = None
