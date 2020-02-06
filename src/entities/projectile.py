import time
from abc import ABC, abstractmethod

from pygame import Vector2
from pygame.surface import Surface

from animation import AnimatedSprite
from constants import PlayerSettings
from enums import ImpactSide, ProjectileState
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from ressource_management import ResourceManagement


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


class TornadoProjectile(Projectile, AnimatedSprite):
    def __init__(self, level: int, player: GameObject):
        sprites = ResourceManagement.get_projectile_slam_sprites(
            Vector2(PlayerSettings.Ability.Slam.AREA_SIZE[0] * {1: 1, 2: 2, 2: 3.60}[
                level], PlayerSettings.Ability.Slam.AREA_SIZE[1])
        )
        first_sprite = next(iter(sprites.values()))[0]

        Projectile.__init__(self, first_sprite)
        AnimatedSprite.__init__(self,
                                ResourceManagement.get_projectile_tornado_sprites(Vector2({1: 50, 2: 200}[level], 30)),
                                3,
                                ProjectileState.DEFAULT)
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
        AnimatedSprite.update(self, delta_time)


class GustProjectile(Projectile, AnimatedSprite):
    def __init__(self):
        surface: Surface = Surface((10, 10))
        surface.fill((0, 255, 255))
        Projectile.__init__(self, surface)
        AnimatedSprite.__init__(self, ResourceManagement.get_projectile_gust_sprites(), 12, ProjectileState.DEFAULT)
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
        AnimatedSprite.update(self, delta_time)


class SlamProjectile(Projectile, AnimatedSprite):
    def __init__(self, level, strength: Vector2):
        sprites = ResourceManagement.get_projectile_slam_sprites(
            Vector2(PlayerSettings.Ability.Slam.AREA_SIZE[0] * {1: 1, 2: 2, 2: 3.60}[
                level], PlayerSettings.Ability.Slam.AREA_SIZE[1])
        )
        first_sprite = next(iter(sprites.values()))[0]

        Projectile.__init__(self, first_sprite)
        AnimatedSprite.__init__(self,
                                ResourceManagement.get_projectile_slam_sprites(
                                    Vector2(PlayerSettings.Ability.Slam.AREA_SIZE[0] * {1: 1, 2: 2, 2: 3.60}[
                                        level], PlayerSettings.Ability.Slam.AREA_SIZE[1])
                                ),
                                12, ProjectileState.DEFAULT)
        self.strength = strength
        self._level = level
        self.__death_time = self._death_time()

    def _death_time(self) -> float:
        return time.time() + PlayerSettings.Ability.Slam.AREA_TIME_TO_LIVE * (1 + self._level * .25)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(self.strength)

    def update(self, delta_time: float):
        AnimatedSprite.update(self, delta_time)
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)
