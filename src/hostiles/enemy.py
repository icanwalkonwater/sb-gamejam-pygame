import time
from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.surface import Surface

from constants import ENEMY_CHILL_WALK_VELOCITY, ENEMY_DETECTION_RANGE_SQR, ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject


class Enemy(RigidPhysicsAwareGameObject, ABC):

    def __init__(self, surface: Surface, weight: float, attack_cooldown: float, target: GameObject,
                 collision_masks: [GameObject] = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, collision_masks)
        self._attack_cooldown: float = attack_cooldown
        self.__cooldown_expire: float = 0
        self._target: GameObject = target
        self._direction = 1

    def update(self, delta_time: float):
        distance_to_target_sqr = self.transform.distance_squared_to(self._target.transform)

        # If too far away, just walk
        if distance_to_target_sqr > ENEMY_DETECTION_RANGE_SQR:
            self.velocity.x = ENEMY_CHILL_WALK_VELOCITY.x * self._direction

        # If in range
        elif time.time() > self.__cooldown_expire:
            if self.attack(delta_time, distance_to_target_sqr):
                self.__cooldown_expire = time.time() + self._attack_cooldown

        RigidPhysicsAwareGameObject.update(self, delta_time)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side)

        if impact_side == ImpactSide.LEFT:
            self._direction = 1
        elif impact_side == ImpactSide.RIGHT:
            self._direction = -1

    @abstractmethod
    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        pass
