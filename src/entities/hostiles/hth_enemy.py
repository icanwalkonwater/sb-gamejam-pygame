from pygame.math import Vector2
from pygame.surface import Surface

from constants import VECTOR2_NULL, EnemySettings
from entities.hostiles.enemy import Enemy
from entities.player import Player
from enums import ImpactSide
from game_object import GameObject
from scene import Scene


class HthEnemy(Enemy):

    def __init__(self):
        surface = Surface((50, 50))
        surface.fill((0, 0, 255))
        Enemy.__init__(self, surface, .5, EnemySettings.HandToHand.HEALTH_MAX,
                       EnemySettings.HandToHand.ATTACK_COOLDOWN_S)
        self.__retreat_distance_sqr: float = 0

    def start(self, scene: Scene):
        Enemy.start(self, scene)
        self.__retreat_distance_sqr = (self.width / 2 + self._target.width / 2) ** 2

    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        if self.is_on_ground and abs(self.velocity.x) < EnemySettings.HandToHand.ATTACK_VELOCITY_X_MAX:
            direction: Vector2 = self._target.center - self.center

            if self.center.distance_squared_to(self._target.center) > self.__retreat_distance_sqr:
                self.__attack_normal(direction)

            return True
        else:
            return False

    def __attack_normal(self, direction: Vector2):
        direction.normalize_ip()
        direction.y -= max(EnemySettings.HandToHand.ATTACK_MIN_JUMP, direction.y)
        direction *= EnemySettings.HandToHand.ATTACK_FACTOR
        self.apply_force(direction)

    def __backoff(self, direction: Vector2):
        if direction == VECTOR2_NULL:
            direction = Vector2(1, 0)
        else:
            direction.normalize_ip()
        direction.y = min(direction.y, .1)
        direction *= EnemySettings.HandToHand.RETREAT_FORCE

        self.apply_force(direction)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if other != self._target:
            Enemy._on_collide(self, other, direction_of_impact, impact_side, delta_time)
        else:
            # Collided with player, he need to suffer
            other: Player
            other.take_damage(10)
            if other.is_dead:
                self._target = None

            self.__backoff(direction_of_impact)
