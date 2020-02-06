from pygame import Vector2
from pygame.surface import Surface

from constants import EnemySettings
from entities.hostiles.enemy import Enemy
from enums import ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from scene import Scene


class HeavyRockEnemy(Enemy):
    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        # i'am not violent !
        pass

    def __init__(self):
        surface = Surface((50, 50))
        surface.fill((100, 100, 100))
        Enemy.__init__(self, surface, EnemySettings.HeavyRock.WIGHT, EnemySettings.HeavyRock.HEALTH_MAX,
                       EnemySettings.HeavyRock.ATTACK_COOLDOWN_S)

    def update(self, delta_time: float):

        # I'am just good guy you kown
        self.move(EnemySettings.HeavyRock.SPEED * self._direction * delta_time)
        RigidPhysicsAwareGameObject.update(self, delta_time)

    def start(self, scene: Scene):
        Enemy.start(self, scene)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        if other != self._target:
            Enemy._on_collide(self, other, direction_of_impact, impact_side, delta_time)
        else:
            if impact_side != ImpactSide.TOP:
                # Collided with player, he need to suffer
                other: GameObject
                if impact_side == ImpactSide.BOTTOM:
                    i = 0
                    other.take_damage(1000)
                elif impact_side == ImpactSide.RIGHT:
                    i = 1
                elif impact_side == ImpactSide.LEFT:
                    i = -1

                other.apply_force(EnemySettings.HeavyRock.KNOCKBACK * i)
                other.take_damage(EnemySettings.HeavyRock.SIDE_DAMAGE)
                if other.is_dead:
                    self._target = None
