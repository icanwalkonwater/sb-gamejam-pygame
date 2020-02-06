from pygame import Surface, Vector2

from entities.player import Player
from enums import ImpactSide
from game_object import GameObject
from physics import PhysicsAwareGameObject, RigidPhysicsAwareGameObject
from scene import Scene
from scene_management import SceneManagement
from ui.information_banner import InformationBanner


class OrbTornado(RigidPhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((255, 50, 50))
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_tornado_jump.level_up()
        text = InformationBanner("Tornado upgraded", "Your Tornado level up to " + str(other.ability_tornado_jump.level), 3)
        text.start(SceneManagement.active_scene)
        self.kill()


class OrbGust(RigidPhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((50, 255, 50))
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_gust.level_up()
        text = InformationBanner("Gust upgraded", "Your Gust level up to " + str(other.ability_gust.level), 3)
        text.start(SceneManagement.active_scene)
        self.kill()


class OrbSlam(RigidPhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((50, 50, 255))
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_slam.level_up()
        text = InformationBanner("Slam upgraded", "Your Slam level up to " + str(other.ability_slam.level), 3)
        text.start(SceneManagement.active_scene)
        self.kill()