import time
from abc import ABC, abstractmethod

from pygame import Vector2
from pygame.surface import Surface

from constants import PlayerSettings
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


class GustProjectile(Projectile):
    def __init__(self):
        surface: Surface = Surface((10, 10))
        surface.fill((0, 255, 255))
        Projectile.__init__(self, surface)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(Vector2(self.velocity.x, PlayerSettings.Ability.Gust.PROJECTILE_HIT_STRENGTH_Y))
        self.kill()


class SlamProjectile(Projectile):
    def __init__(self, strength: Vector2):
        image: Surface = Surface((PlayerSettings.Ability.Slam.AREA_SIZE[0], PlayerSettings.Ability.Slam.AREA_SIZE[1]))
        image.fill((0, 255, 0))
        Projectile.__init__(self, image)
        self.strength = strength
        self.__death_time = time.time() + PlayerSettings.Ability.Slam.AREA_TIME_TO_LIVE

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(self.strength)
        self.kill()

    def update(self, delta_time: float):
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)
