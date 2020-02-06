from pygame import Vector2

from animation import AnimatedSprite
from constants import EnemySettings
from entities.hostiles.enemy import Enemy
from enums import ImpactSide, EnemyState
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from ressource_management import ResourceManagement
from scene import Scene


class HeavyRockEnemy(Enemy, AnimatedSprite):
    def __init__(self):
        sprites = ResourceManagement.get_enemy_stone_sprites()
        sprite = next(iter(sprites.values()))[0]
        Enemy.__init__(self, sprite, EnemySettings.HeavyRock.WEIGHT, EnemySettings.HeavyRock.HEALTH_MAX,
                       EnemySettings.HeavyRock.ATTACK_COOLDOWN_S)
        AnimatedSprite.__init__(self, sprites, 2, EnemyState.RUNNING_LEFT)

    def attack(self, delta_time: float, distance_sqr: float) -> bool:
        # i'am not violent !
        pass

    def update(self, delta_time: float):

        # I'am just good guy you kown
        self.move(EnemySettings.HeavyRock.SPEED * self._direction * delta_time)
        self._state = (EnemyState.RUNNING_LEFT if self._direction < 0 else EnemyState.RUNNING_RIGHT)
        RigidPhysicsAwareGameObject.update(self, delta_time)
        AnimatedSprite.update(self, delta_time)

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
