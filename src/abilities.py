import time
from abc import ABC

from pygame import Vector2

from constants import PlayerSettings
from entities.projectile import GustProjectile, SlamProjectile
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from scene import Scene
from scene_management import SceneManagement


class Ability(ABC):

    def __init__(self, level: int = PlayerSettings.Ability.BASE_LEVEL,
                 cooldown: float = PlayerSettings.Ability.BASE_COOLDOWN):
        self.level: int = level
        self.cooldown: float = cooldown
        self._next_usage: float = 0


class TornadoJumpAbility(Ability):

    def __init__(self, level: int, mana_cost: float = PlayerSettings.Ability.TornadoJump.MANA_COST):
        Ability.__init__(self, level, PlayerSettings.Ability.TornadoJump.COOLDOWN)
        self.mana_cost = mana_cost

    def use(self, player: RigidPhysicsAwareGameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            player.apply_force(Vector2(0, PlayerSettings.Ability.TornadoJump.STRENGTH))
            self._next_usage = time.time() + self.cooldown


class GustAbility(Ability):

    def __init__(self, level: int = PlayerSettings.Ability.BASE_LEVEL,
                 cooldown: float = PlayerSettings.Ability.BASE_COOLDOWN,
                 mana_cost: float = PlayerSettings.Ability.Gust.MANA_COST):
        Ability.__init__(self, level, cooldown)
        self.mana_cost = mana_cost

    def _gust_strength_calc(self) -> Vector2:
        return Vector2(PlayerSettings.Ability.Gust.STRENGTH * self.level ** 2, 0)

    def _gust_backward_strength_calc(self) -> Vector2:
        return Vector2(PlayerSettings.Ability.Gust.KNOCKBACK_STRENGTH / self.level, 0)

    def use(self, player: RigidPhysicsAwareGameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            scene: Scene = SceneManagement.active_scene

            gust_projectile: GustProjectile = GustProjectile()
            gust_projectile.add_to_collision_mask(scene.environment, scene.enemies)
            gust_projectile.move(Vector2(player.transform.x + player.width, player.transform.y + 10))

            scene.projectiles.add(gust_projectile)
            scene.dynamics.add(gust_projectile)

            gust_projectile.apply_force(self._gust_strength_calc())
            player.apply_force(self._gust_backward_strength_calc())

            self._next_usage = time.time() + self.cooldown


class SlamAbility(Ability):

    def __init__(self, level: int, cooldown: float = PlayerSettings.Ability.BASE_COOLDOWN,
                 mana_cost: float = PlayerSettings.Ability.Slam.MANA_COST):
        Ability.__init__(self, level, cooldown)
        self.mana_cost = mana_cost

    def _slam_strength_calc(self) -> Vector2:
        return Vector2(0, PlayerSettings.Ability.Slam.STRENGTH * self.level ** 2)

    @staticmethod
    def _slam_position_calc(player: GameObject) -> Vector2:
        return Vector2(player.transform.x - (PlayerSettings.Ability.Slam.AREA_SIZE[0] / 2 - player.width),
                       player.transform.y + player.height - PlayerSettings.Ability.Slam.AREA_SIZE[1])

    def use(self, player: RigidPhysicsAwareGameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            scene: Scene = SceneManagement.active_scene
            projectile_slam: SlamProjectile = SlamProjectile(self._slam_strength_calc())

            projectile_slam.add_to_collision_mask(scene.enemies)

            scene.projectiles.add(projectile_slam)
            scene.dynamics.add(projectile_slam)

            projectile_slam.move(SlamAbility._slam_position_calc(player))
            self._next_usage = time.time() + self.cooldown
