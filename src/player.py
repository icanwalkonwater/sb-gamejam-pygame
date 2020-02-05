from pygame import Vector2, Surface

from ability import TornadoJumpAbility, GustAbility, SlamAbility
from constants import ImpactSide, PLAYER_DAMAGE_REPULSION_FACTOR, PLAYER_MANA_MAX, PLAYER_MANA_WALK_REGENERATION_FACTOR
from game_object import GameObject
from hostiles.enemy import Enemy
from keyboard_input import InputController
from physics import RigidPhysicsAwareGameObject


class Player(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, collides_with: [GameObject] = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, collides_with)
        self._ability_tornado_jump = TornadoJumpAbility(1)
        self._ability_gust = GustAbility()
        self._ability_slam = SlamAbility(1, 1)
        self._mana_level: float = PLAYER_MANA_MAX

    def update(self, delta_time: float):
        RigidPhysicsAwareGameObject.update(self, delta_time)

        motion = InputController.get_motion() * delta_time
        powers = InputController.get_powers()

        if powers[0]:
            self._ability_gust.use(self)
        if powers[1]:
            self._ability_slam.use(self)

        # Apply left/right controls
        if motion.x != 0:
            self.apply_force(Vector2(motion.x, 0))

        if motion.y < 0 and self.is_on_ground:
            self.is_on_ground = False
            self._ability_tornado_jump.use(self)

        if self._mana_level < PLAYER_MANA_MAX:
            self._mana_level += self.velocity.magnitude() * PLAYER_MANA_WALK_REGENERATION_FACTOR * delta_time
            self._mana_level = min(self._mana_level, PLAYER_MANA_MAX)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        # Common collision with something normal
        if not isinstance(other, Enemy):
            RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side)
        elif direction_of_impact != Vector2(0, 0):
            # Collided with an enemy
            other: Enemy
            direction_of_impact.normalize_ip()
            self.apply_force(direction_of_impact * PLAYER_DAMAGE_REPULSION_FACTOR)
