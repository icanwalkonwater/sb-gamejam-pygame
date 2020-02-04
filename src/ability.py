import time
from abc import ABC

from pygame import Vector2

from constants import PLAYER_ABILITY_BASE_LEVEL, PLAYER_ABILITY_BASE_COOLDOWN, PLAYER_ABILITY_GUST_BASE_STRENGTH, \
    PLAYER_ABILITY_GUST_BASE_KNOCKBACK_STRENGTH, PLAYER_ABILITY_SLAM_BASE_STRENGTH, PLAYER_ABILITY_TORNADO_JUMP_COOLDOWN, \
    PLAYER_ABILITY_TORNADO_JUMP_STRENGTH, PLAYER_ABILITY_SLAM_BASE_AREA, PLAYER_ABILITY_SLAM_HEIGHT
from game_object import GameObject
from projectile import GustProjectile, SlamProjectile
from scene import Scene
from scene_management import SceneManagement


class Ability(ABC):

    def __init__(self, level: int = PLAYER_ABILITY_BASE_LEVEL, cooldown: float = PLAYER_ABILITY_BASE_COOLDOWN):
        self.level: int = level
        self.cooldown: float = cooldown
        self._next_usage: float = time.time()


class TornadoJumpAbility(Ability):

    def __init__(self, level: int):
        Ability.__init__(self, level, PLAYER_ABILITY_TORNADO_JUMP_COOLDOWN)

    def use(self, player: GameObject):
        if self._next_usage <= time.time():
            player.apply_force(Vector2(0, PLAYER_ABILITY_TORNADO_JUMP_STRENGTH))
            self._next_usage = time.time() + self.cooldown


class GustAbility(Ability):

    def __init__(self, level: int, cooldown: float = None):
        Ability.__init__(self, level, cooldown)

    def _gust_strength_calc(self) -> Vector2:
        return Vector2(PLAYER_ABILITY_GUST_BASE_STRENGTH * self.level ** 2, 0)

    def _gust_backward_strength_calc(self) -> Vector2:
        return Vector2(PLAYER_ABILITY_GUST_BASE_KNOCKBACK_STRENGTH / self.level, 0)

    def use(self, player: GameObject):
        if self._next_usage <= time.time():
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

    def __init__(self, level: int, cooldown: float = None):
        Ability.__init__(self, level, cooldown)

    def _slam_strength_calc(self) -> Vector2:
        return Vector2(0, PLAYER_ABILITY_SLAM_BASE_STRENGTH * self.level ** 2)

    @staticmethod
    def _slam_position_calc(player: GameObject) -> Vector2:
        return Vector2(player.transform.x - (PLAYER_ABILITY_SLAM_BASE_AREA / 2 - player.width),
                       player.transform.y + player.height - PLAYER_ABILITY_SLAM_HEIGHT)

    def use(self, player: GameObject):
        if self._next_usage <= time.time():
            scene: Scene = SceneManagement.active_scene
            projectile_slam: SlamProjectile = SlamProjectile(self._slam_strength_calc())

            projectile_slam.add_to_collision_mask(scene.enemies)

            scene.projectiles.add(projectile_slam)
            scene.dynamics.add(projectile_slam)

            projectile_slam.move(SlamAbility._slam_position_calc(player))
            self._next_usage = time.time() + self.cooldown
