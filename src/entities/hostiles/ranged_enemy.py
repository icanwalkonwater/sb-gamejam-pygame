import time

from pygame import Vector2
from pygame.surface import Surface

from constants import EnemySettings
from entities.hostiles.enemy import Enemy
from entities.player import Player
from entities.projectile import Projectile
from enums import ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from scene import Scene
from scene_management import SceneManagement


class RangedEnemy(Enemy):
    def __init__(self):
        surface = Surface((50, 50))
        surface.fill((255, 0, 0))
        Enemy.__init__(self, surface, EnemySettings.Ranged.WEIGHT, EnemySettings.Ranged.HEALTH_MAX,
                       EnemySettings.Ranged.ATTACK_COOLDOWN_S)
        self.__cooldown_expire = 0

    def start(self, scene: Scene):
        Enemy.start(self, scene)
        self.__cooldown_expire = 0

    def _target_direction(self) -> int:
        diff = self.center.x - self._target.center.x
        if diff <= 0:
            return -1
        else:
            return 1

    def attack(self):
        scene = SceneManagement.active_scene
        enemy_projectile: EnemyProjectile = EnemyProjectile(self._target.center - self.center)
        enemy_projectile.start(scene)
        enemy_projectile.move(self.center)
        self.__cooldown_expire = time.time() + EnemySettings.Ranged.ATTACK_COOLDOWN_S

    def update(self, delta_time: float):
        distance_to_target_sqr = EnemySettings.Ranged.DETECTION_RANGE_SQR + 1 if self._target is None else \
            self.center.distance_squared_to(self._target.center)

        # If too far away, just walk
        if distance_to_target_sqr > EnemySettings.Ranged.DETECTION_RANGE_SQR and self.is_on_ground:
            self.move(EnemySettings.CHILL_WALK_VELOCITY * self._direction * delta_time)

        # If the player is on fear range run in the opposite direction
        elif distance_to_target_sqr < EnemySettings.Ranged.FEAR_RANGE_SQR and self.is_on_ground:
            self.move(EnemySettings.Ranged.FEAR_WALK_VELOCITY * self._target_direction() * delta_time)

        # If in range
        elif time.time() > self.__cooldown_expire:
            self.attack()

        RigidPhysicsAwareGameObject.update(self, delta_time)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide,
                    delta_time: float):
        RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side, delta_time)
        if other != self._target:
            Enemy._on_collide(self, other, direction_of_impact, impact_side, delta_time)


class EnemyProjectile(Projectile):
    @staticmethod
    def _death_time() -> float:
        return time.time() + EnemySettings.Ranged.Projectile.TIME_TO_LIVE

    def start(self, scene):
        self.add_to_collision_mask(scene.player, scene.environment)
        scene.projectiles.add(self)
        scene.dynamics.add(self)
        self.apply_force(self._direction * 30)

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
