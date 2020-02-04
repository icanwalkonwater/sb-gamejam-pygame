from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from constants import ENEMY_CHILL_WALK_VELOCITY, ENEMY_DETECTION_RANGE, ImpactSide
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject


class Enemy(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, target: GameObject, ground: [GameObject] = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, ground)
        self._target: GameObject = target
        self._direction = 1

    def update(self, delta_time: float):
        collision_mask: Rect = ENEMY_DETECTION_RANGE.move(
            self.transform.x - ENEMY_DETECTION_RANGE.width / 2,
            self.transform.y + ENEMY_DETECTION_RANGE.height / 2
        )

        if not self._target.rect.colliderect(collision_mask):
            self.velocity.x = ENEMY_CHILL_WALK_VELOCITY.x * self._direction
            pass
        else:
            print('AAAAA')

        RigidPhysicsAwareGameObject.update(self, delta_time)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side)

        if impact_side == ImpactSide.LEFT:
            self._direction = 1
        elif impact_side == ImpactSide.RIGHT:
            self._direction = -1
