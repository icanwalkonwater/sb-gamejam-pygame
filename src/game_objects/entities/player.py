from pygame import Vector2

from game_objects.abilities import TornadoJumpAbility, GustAbility, SlamAbility
from game_objects.animation import AnimatedSprite
from constants import PlayerSettings, VECTOR2_NULL
from game_objects.entities.hostiles.enemy import Enemy
from game_objects.entities.hostiles.heavy_rock_enemy import HeavyRockEnemy
from game_objects.entities.hostiles.hth_enemy import HthEnemy
from game_objects.entities.living_entity import LivingEntity
from enums import ImpactSide, PlayerState
from game_objects.game_object import GameObject
from keyboard_input import InputController
from game_objects.physics import RigidPhysicsAwareGameObject
from ressource_management import ResourceManagement
from scene import Scene


class Player(RigidPhysicsAwareGameObject, LivingEntity, AnimatedSprite):

    def __init__(self, weight: float = .5):
        sprites = ResourceManagement.get_player_sprites()
        first_sprite = next(iter(sprites.values()))[0]

        RigidPhysicsAwareGameObject.__init__(self, first_sprite, weight)
        LivingEntity.__init__(self, PlayerSettings.HEALTH_MAX, invincibility_duration=1)
        AnimatedSprite.__init__(self, sprites, 3, PlayerState.IDLE)
        self.ability_tornado_jump = TornadoJumpAbility(1)
        self.ability_gust = GustAbility(1)
        self.ability_slam = SlamAbility(1, 1)
        self.mana: float = PlayerSettings.MANA_MAX
        self._last_direction = 1

    def start(self, scene: Scene):
        LivingEntity.start(self)
        scene.player.add(self)
        self.add_to_collision_mask(scene.environment, scene.enemies)

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
        if not self.is_on_ground:
            self._state = PlayerState.FLYING
        elif self.velocity == VECTOR2_NULL:
            self._state = PlayerState.IDLE
        elif self._last_direction > 0:
            self._state = PlayerState.RUNNING_RIGHT
        elif self._last_direction < -0:
            self._state = PlayerState.RUNNING_LEFT

    def __update_controls(self, delta_time: float):

        motion = InputController.get_motion() * delta_time
        powers = InputController.get_powers()  # One shot controls, no need to use delta time

        # Use abilities
        if powers[0]:
            self.ability_gust.use(self)
        if powers[1]:
            self.ability_slam.use(self)

        # Apply left/right controls
        if motion.x != 0:
            self.apply_force(Vector2(motion.x, 0))

        # Keep track of the last direction we were looking at
        if motion.x < 0:
            self._last_direction = -1
        elif motion.x > 0:
            self._last_direction = 1

        # Jump
        if motion.y < 0 and self.is_on_ground:
            self.is_on_ground = False
            self.ability_tornado_jump.use(self)

    def __update_mana_regeneration(self, delta_time: float):
        if self.mana < PlayerSettings.MANA_MAX:
            self.mana += self.velocity.magnitude() * PlayerSettings.MANA_PASSIVE_REGENERATION_FACTOR * delta_time
            self.mana = min(self.mana, PlayerSettings.MANA_MAX)

    def _die(self):
        self.kill()

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        # Common collision with something normal
        if isinstance(other, HthEnemy):
            if direction_of_impact != VECTOR2_NULL:
                # Collided with an enemy
                other: Enemy
                # Apply knockback
                direction_of_impact.normalize_ip()
                self.apply_force(direction_of_impact * PlayerSettings.DAMAGE_REPULSION_FACTOR)
        elif isinstance(other, Enemy):
            if isinstance(other, HeavyRockEnemy) and impact_side == ImpactSide.BOTTOM:
                RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side, delta_time)
            else:
                pass
        else:
            RigidPhysicsAwareGameObject._on_collide(self, other, direction_of_impact, impact_side, delta_time)
