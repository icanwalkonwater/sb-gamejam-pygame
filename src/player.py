from pygame import Vector2, Surface

from constants import PLAYER_JUMP_FORCE, ImpactSide, PLAYER_DAMAGE_REPULSION_FACTOR
from game_object import GameObject
from hostiles.enemy import Enemy
from keyboard_input import InputController
from physics import RigidPhysicsAwareGameObject


class Player(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, collides_with: [GameObject] = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, collides_with)

    def update(self, delta_time: float):
        RigidPhysicsAwareGameObject.update(self, delta_time)

        motion = InputController.get_motion() * delta_time

        if motion.x != 0:
            self.apply_force(Vector2(motion.x, 0))

        if motion.y < 0 and self.is_on_ground:
            self.jump()

    def jump(self):
        self.is_on_ground = False
        self.apply_force(PLAYER_JUMP_FORCE)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        # Common collision with something normal
        if not isinstance(other, Enemy):
            RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side)
        elif direction_of_impact.len:
            # Collided with an enemy
            other: Enemy
            direction_of_impact.normalize_ip()
            self.apply_force(direction_of_impact * PLAYER_DAMAGE_REPULSION_FACTOR)
