import random
import time
from abc import ABC, abstractmethod

from pygame import Vector2
from pygame.surface import Surface

from constants import PlayerSettings, EnemySettings
from entities.player import Player
from enums import ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject


class Hitable(ABC):

    @abstractmethod
    def on_hit(self, projectile, impact_side: ImpactSide, strenght: Vector2):
        pass


class Projectile(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface):
        RigidPhysicsAwareGameObject.__init__(self, surface, 0)
        self.resistance_amount = 0

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, Hitable):
            other.on_hit(self, impact_side)
        self.kill()


class TornadoProjectile(Projectile):
    def __init__(self, image: Surface, level: int, player: GameObject):
        Projectile.__init__(self, image)
        self.___death_time = time.time() + PlayerSettings.Ability.TornadoJump.TIME_TO_LIVE
        self._player = player
        self.level = level

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, direction: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(
                direction_of_impact.normalize() * PlayerSettings.Ability.TornadoJump.KNOCKBACK_STRENGTH * self.level)

    def update(self, delta_time: float):
        if self.___death_time <= time.time():
            self.kill()
        else:
            self.center = self._player.center
            self.transform.y = self._player.rect.bottom - self.height / 2
            Projectile.update(self, delta_time)


class GustProjectile(Projectile):
    def __init__(self):
        surface: Surface = Surface((10, 10))
        surface.fill((0, 255, 255))
        Projectile.__init__(self, surface)
        self.__death_time = time.time() + PlayerSettings.Ability.Gust.TIME_TO_LIVE

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(Vector2(self.velocity.x, PlayerSettings.Ability.Gust.PROJECTILE_HIT_STRENGTH_Y))
        self.kill()

    def update(self, delta_time: float):
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)


class SlamProjectile(Projectile):
    def __init__(self, surface: Surface, level: int, strength: Vector2):
        Projectile.__init__(self, surface)
        self.strength = strength
        self._level = level
        self.__death_time = self._death_time()

    def _death_time(self) -> float:
        return time.time() + PlayerSettings.Ability.Slam.AREA_TIME_TO_LIVE * (1 + self._level * .25)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(self.strength)
        self.kill()

    def update(self, delta_time: float):
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)


class EnemyProjectile(Projectile):
    @staticmethod
    def _death_time() -> float:
        return time.time() + EnemySettings.Ranged.Projectile.TIME_TO_LIVE

    def start(self, scene):
        self.add_to_collision_mask(scene.player, scene.environment)
        scene.projectiles.add(self)
        scene.dynamics.add(self)
        self.apply_force(self.direction * 30)

    def __init__(self, direction: Vector2):
        sprite = Surface((10, 10))
        sprite.fill((125, 125, 0))
        Projectile.__init__(self, sprite)
        self.__death_time = EnemyProjectile._death_time()
        self._direction = direction

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, Player):
            other.apply_force(self._direction * 30)
            other.take_damage(20)
        self.kill()

    def update(self, delta_time: float):
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)
