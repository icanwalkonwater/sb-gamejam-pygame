import time
from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.surface import Surface

from constants import EnemySettings
from entities.living_entity import LivingEntity
from enums import ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from scene import Scene


class Enemy(RigidPhysicsAwareGameObject, LivingEntity, ABC):

    def __init__(self, surface: Surface, weight: float, max_health: float, attack_cooldown: float,
                 damage_reduction: float = 0):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight)
        LivingEntity.__init__(self, max_health, damage_reduction)
        self._attack_cooldown: float = attack_cooldown
        self.__cooldown_expire: float = 0
        self._target: GameObject = None
        self._direction = 1

    def start(self, scene: Scene):
        LivingEntity.start(self)
        self.__cooldown_expire = 0
        self._direction = 1
        self._target = scene.player.sprite

        scene.enemies.add(self)
        self.add_to_collision_mask(scene.environment, scene.player)

    def update(self, delta_time: float):
        distance_to_target_sqr = EnemySettings.DETECTION_RANGE_SQR + 1 if self._target is None else \
            self.center.distance_squared_to(self._target.center)

        # If too far away, just walk
        if distance_to_target_sqr > EnemySettings.DETECTION_RANGE_SQR and self.is_on_ground:
            self.move(EnemySettings.CHILL_WALK_VELOCITY * self._direction * delta_time)

        # If in range
        elif time.time() > self.__cooldown_expire:
            if self.attack(delta_time, distance_to_target_sqr):
                self.__cooldown_expire = time.time() + self._attack_cooldown

        RigidPhysicsAwareGameObject.update(self, delta_time)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        collision_damage = LivingEntity._velocity_to_damage(self.velocity)
        if collision_damage > 0:
            self.take_damage(collision_damage)

        RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side, delta_time)

        if impact_side == ImpactSide.LEFT:
            self._direction = 1
        elif impact_side == ImpactSide.RIGHT:
            self._direction = -1

    def _die(self):
        self.kill()

    @abstractmethod
    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        pass
