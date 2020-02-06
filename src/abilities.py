import time
from abc import ABC

from pygame import Vector2, Surface

from constants import PlayerSettings
from entities.projectile import GustProjectile, SlamProjectile, TornadoProjectile
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

    def _create_tornado_surface(self) -> Surface:  # TODO remplacr par les srpite
        if self.level == 1:
            sprite: Surface = Surface((50, 30))
            sprite.fill((0, 0, 255))
        else:
            sprite: Surface = Surface((200,30))
            sprite.fill((0, 0, 255))

        return sprite

    def use(self, player: GameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            tornado_projectile_sprite: Surface = self._create_tornado_surface()
            tornado_projectile: TornadoProjectile = TornadoProjectile(tornado_projectile_sprite, self.level, player)

            scene: Scene = SceneManagement.active_scene
            tornado_projectile.move(Vector2(player.center.x - tornado_projectile.width / 2, player.transform.y))
            tornado_projectile.add_to_collision_mask(scene.enemies)

            scene.projectiles.add(tornado_projectile)
            scene.dynamics.add(tornado_projectile)

            player.apply_force(Vector2(0, PlayerSettings.Ability.TornadoJump.STRENGTH))
            self._next_usage = time.time() + self.cooldown


class GustAbility(Ability):

    def __init__(self, level: int = PlayerSettings.Ability.BASE_LEVEL,
                 cooldown: float = PlayerSettings.Ability.BASE_COOLDOWN,
                 mana_cost: float = PlayerSettings.Ability.Gust.MANA_COST):
        Ability.__init__(self, level, cooldown)
        self.mana_cost = mana_cost

    def _gust_strength_calc(self,player: GameObject) -> Vector2:
        return Vector2(PlayerSettings.Ability.Gust.STRENGTH *  player._last_direction, 0)

    def _gust_backward_strength_calc(self, player: GameObject) -> Vector2:
        return Vector2(PlayerSettings.Ability.Gust.KNOCKBACK_STRENGTH / self.level * player._last_direction, 0)

    def use(self, player: RigidPhysicsAwareGameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            scene: Scene = SceneManagement.active_scene

            gust_projectile: GustProjectile = GustProjectile()
            gust_projectile.add_to_collision_mask(scene.environment, scene.enemies)
            gust_projectile.move(Vector2(player.transform.x + player.width, player.transform.y + 10))

            scene.projectiles.add(gust_projectile)
            scene.dynamics.add(gust_projectile)

            gust_projectile.apply_force(self._gust_strength_calc(player))
            player.apply_force(self._gust_backward_strength_calc(player))

            self._next_usage = time.time() + self.cooldown


class SlamAbility(Ability):

    def __init__(self, level: int, cooldown: float = PlayerSettings.Ability.BASE_COOLDOWN,
                 mana_cost: float = PlayerSettings.Ability.Slam.MANA_COST):
        Ability.__init__(self, level, cooldown)
        self.mana_cost = mana_cost

    def _slam_strength_calc(self) -> Vector2:
        return Vector2(0, PlayerSettings.Ability.Slam.STRENGTH * (1 + self.level * .5))

    def _create_slame_surface(self) -> Surface:  # TODO remplacer les calcules par des sprite de la taille en question
        if self.level == 1:
            sprite: Surface = Surface(PlayerSettings.Ability.Slam.AREA_SIZE)
        elif self.level == 2:
            sprite: Surface = Surface((PlayerSettings.Ability.Slam.AREA_SIZE[0] * 2, PlayerSettings.Ability.Slam.AREA_SIZE[1]))
        elif self.level == 3:
            sprite: Surface = Surface((PlayerSettings.Ability.Slam.AREA_SIZE[0] * 2 *1.80,PlayerSettings.Ability.Slam.AREA_SIZE[1]))

        return sprite

    def _slam_position_calc(self, player: GameObject, surface: Surface) -> Vector2:
        x = player.center.x
        if self.level == 1:
            if player._last_direction == -1:
                x -= surface.get_width()

        if self.level >= 2:
            x -= surface.get_width() / 2

        return Vector2(x, player.transform.y - surface.get_height() + player.height)

    def use(self, player: RigidPhysicsAwareGameObject):
        if self._next_usage <= time.time() and player.mana > self.mana_cost:
            player.mana -= self.mana_cost
            scene: Scene = SceneManagement.active_scene
            projectile_slam_surface = self._create_slame_surface()
            projectile_slam: SlamProjectile = SlamProjectile(projectile_slam_surface, self.level,
                                                             self._slam_strength_calc())

            projectile_slam.add_to_collision_mask(scene.enemies)

            scene.projectiles.add(projectile_slam)
            scene.dynamics.add(projectile_slam)

            projectile_slam.move(self._slam_position_calc(player, projectile_slam_surface))

            self._next_usage = time.time() + self.cooldown
