from pygame.math import Vector2
from pygame.surface import Surface

from constants import ENEMY_HTH_ATTACK_VELOCITY_X_MAX, ENEMY_HTH_ATTACK_MIN_JUMP, ENEMY_HTH_RETREAT_DISTANCE_SQR, \
    ENEMY_HTH_RETREAT_FORCE, ENEMY_HTH_ATTACK_COOLDOWN
from game_object import GameObject
from hostiles.enemy import Enemy


class HthEnemy(Enemy):

    def __init__(self, target: GameObject):
        surface = Surface((50, 50))
        surface.fill((0, 0, 255))
        Enemy.__init__(self, surface, .5, ENEMY_HTH_ATTACK_COOLDOWN, target=target)

    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        if self.is_on_ground and abs(self.velocity.x) < ENEMY_HTH_ATTACK_VELOCITY_X_MAX:
            direction: Vector2 = self._target.transform - self.transform

            if distance_sqr == 0:
                # Ignore if the enemy is right of top of us
                pass
            elif self.transform.distance_squared_to(self._target.transform) > ENEMY_HTH_RETREAT_DISTANCE_SQR:
                direction.normalize_ip()
                direction.y -= max(ENEMY_HTH_ATTACK_MIN_JUMP, direction.y)
                direction *= 3000
                self.apply_force(direction)
            else:
                direction.normalize_ip()
                direction *= ENEMY_HTH_RETREAT_FORCE
                self.apply_force(direction)

            return True
        else:
            return False
