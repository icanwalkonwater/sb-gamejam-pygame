import time
from abc import ABC, abstractmethod

from pygame import Vector2
from pygame.surface import Surface

from game_object import GameObject, Moveable

from physics import RigidPhysicsAwareGameObject, ImpactSide

from constants import PLAYER_ABILITY_SLAM_TIME_TO_LIVE, PLAYER_ABILITY_SLAM_WIDTH, PLAYER_ABILITY_SLAM_HEIGHT, PLAYER_ABILITY_GUST_UPWARD_STRENGTH


class Hitable(ABC):

    @abstractmethod
    def on_hit(self, projectile, impact_side: ImpactSide, strenght: Vector2):
        pass


class Projectile(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, collides_with: [GameObject]):
        RigidPhysicsAwareGameObject.__init__(self, surface, 0, collides_with)
        self.resistance_amount = 0

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, Hitable):
            other.on_hit(self, impact_side)
        self.kill()


class GustProjectile(Projectile):
    def __init__(self, collides_with: [GameObject] = None):
        surface: Surface = Surface((10, 10))
        surface.fill((0, 255, 255))
        Projectile.__init__(self, surface, collides_with)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(Vector2(self.velocity.x, PLAYER_ABILITY_GUST_UPWARD_STRENGTH))
        self.kill()


class SlamProjectile(Projectile):
    def __init__(self, strength: Vector2, collides_with: [GameObject] = None):
        image: Surface = Surface((PLAYER_ABILITY_SLAM_WIDTH, PLAYER_ABILITY_SLAM_HEIGHT))
        image.fill((0, 255, 0))
        Projectile.__init__(self, image, collides_with)
        self.strength = strength
        self.__death_time = time.time() + PLAYER_ABILITY_SLAM_TIME_TO_LIVE

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        if isinstance(other, RigidPhysicsAwareGameObject):
            other.apply_force(self.strength)
        self.kill()

    def update(self, delta_time: float):
        if self.__death_time <= time.time():
            self.kill()
        else:
            Projectile.update(self, delta_time)
