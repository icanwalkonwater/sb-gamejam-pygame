import time

from pygame.surface import Surface

from constants import EnemySettings
from entities.hostiles.enemy import Enemy
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject


class RanEnemy(Enemy):
    def __init__(self, target: GameObject):
        surface = Surface((50, 50))
        surface.fill((255, 0, 0))
        Enemy.__init__(self, surface, EnemySettings.Ranged.WIEGHT, EnemySettings.Ranged.HEALTH_MAX,
                       EnemySettings.Ranged.ATTACK_COOLDOWN_S, target)

    def _target_direction(self) -> int:
        diff = self.center.x - self._target.center.x
        if diff >= 0:
            return 1
        else:
            return 0

    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        pass

    def update(self, delta_time: float):
        distance_to_target_sqr = EnemySettings.Ranged.DETECTION_RANGE_SQR + 1 if self._target is None else \
            self.center.distance_squared_to(self._target.center)

        # If too far away, just walk
        if distance_to_target_sqr > EnemySettings.Ranged.DETECTION_RANGE_SQR and self.is_on_ground:
            self.move(EnemySettings.CHILL_WALK_VELOCITY * self._direction * delta_time)

        # If the player is on fear range run in the opposite direction
        elif distance_to_target_sqr > EnemySettings.Ranged.FEAR_RANGE_SQR and self.is_on_ground:
            self.move(EnemySettings.Ranged.FEAR_WALK_VELOCITY * self._target_direction() * -1 * delta_time)

        # If in range
        elif time.time() > self.__cooldown_expire:
            if self.attack(delta_time, distance_to_target_sqr):
                self.__cooldown_expire = time.time() + self._attack_cooldown

        RigidPhysicsAwareGameObject.update(self, delta_time)
