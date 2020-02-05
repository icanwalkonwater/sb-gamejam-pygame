from enum import Enum

from pygame import Vector2, Surface

from abilities import TornadoJumpAbility, GustAbility, SlamAbility
from animation import AnimatedSprite
from constants import ImpactSide, PLAYER_DAMAGE_REPULSION_FACTOR, PLAYER_MANA_MAX, PLAYER_MANA_WALK_REGENERATION_FACTOR, \
    PLAYER_HEALTH_MAX
from entities.hostiles.enemy import Enemy
from entities.living_entity import LivingEntity
from game_object import GameObject
from keyboard_input import InputController
from physics import RigidPhysicsAwareGameObject


class PlayerState(Enum):
    IDLE = 1
    RUNNING_LEFT = 2
    RUNNING_RIGHT = 3
    FLYING = 4


class Player(RigidPhysicsAwareGameObject, LivingEntity, AnimatedSprite):

    def __init__(self, surface: Surface, weight: float, collides_with: [GameObject] = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, collides_with)
        LivingEntity.__init__(self, PLAYER_HEALTH_MAX, invincibility_duration=1)
        AnimatedSprite.__init__(self, {
            PlayerState.IDLE: ["wizard_idle_1.png", "wizard_idle_2.png"],
            PlayerState.RUNNING_RIGHT: ["wizard_running_1R.png", "wizard_running_2R.png"],
            PlayerState.RUNNING_LEFT: ["wizard_running_1L.png", "wizard_running_2L.png"],
            PlayerState.FLYING: ["wizard_flying.png"]
        }, 3, PlayerState.IDLE)
        self._ability_tornado_jump = TornadoJumpAbility(1)
        self._ability_gust = GustAbility()
        self._ability_slam = SlamAbility(1, 1)
        self.mana: float = PLAYER_MANA_MAX

    def update(self, delta_time: float):
        # Update controls
        self.__update_controls(delta_time)

        # Passive mana regeneration
        self.__update_mana_regeneration(delta_time)

        # Finally, apply physics
        RigidPhysicsAwareGameObject.update(self, delta_time)

        # Update the state
        self.__update_state()
        AnimatedSprite.update(self, delta_time)

    def __update_state(self):
        print(self._state)
        if not self.is_on_ground:
            self._state = PlayerState.FLYING
        elif self.velocity.x > 0:
            self._state = PlayerState.RUNNING_RIGHT
        elif self.velocity.x < -0:
            self._state = PlayerState.RUNNING_LEFT
        else:
            self._state = PlayerState.IDLE

    def __update_controls(self, delta_time: float):

        motion = InputController.get_motion() * delta_time
        powers = InputController.get_powers()  # One shot controls, no need to use delta time

        # Use abilities
        if powers[0]:
            self._ability_gust.use(self)
        if powers[1]:
            self._ability_slam.use(self)

        # Apply left/right controls
        if motion.x != 0:
            self.apply_force(Vector2(motion.x, 0))

        # Jump
        if motion.y < 0 and self.is_on_ground:
            self.is_on_ground = False
            self._ability_tornado_jump.use(self)

    def __update_mana_regeneration(self, delta_time: float):
        if self.mana < PLAYER_MANA_MAX:
            self.mana += self.velocity.magnitude() * PLAYER_MANA_WALK_REGENERATION_FACTOR * delta_time
            self.mana = min(self.mana, PLAYER_MANA_MAX)

    def _die(self):
        print("Die")
        self.kill()

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        # Common collision with something normal
        if not isinstance(other, Enemy):
            RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side)
        elif direction_of_impact != Vector2(0, 0):
            # Collided with an enemy
            other: Enemy
            # Apply knockback
            direction_of_impact.normalize_ip()
            self.apply_force(direction_of_impact * PLAYER_DAMAGE_REPULSION_FACTOR)
