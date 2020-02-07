from pygame import Surface, Vector2

from enums import ImpactSide
from game_objects.entities.player import Player
from game_objects.game_object import GameObject
from game_objects.physics import RigidPhysicsAwareGameObject
from ressource_management import ResourceManagement
from scene import Scene
from scene_management import SceneManagement
from ui.information_banner import InformationBanner


class OrbTornado(RigidPhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = ResourceManagement.get_image('orb_jump.png')
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        self.kill()
        other: Player
        other.ability_tornado_jump.level_up()
        text = InformationBanner('TORNADO JUMP UPGRADED !',
                                 'TORNADO JUMP LVL ' + str(other.ability_tornado_jump.level), 3)
        text.start(SceneManagement.active_scene)

    def update(self, delta_time: float):
        RigidPhysicsAwareGameObject.update(self, delta_time)


class OrbGust(RigidPhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = ResourceManagement.get_image('orb_gust.png')
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_gust.level_up()
        text = InformationBanner('GUST UPGRADED !', 'GUST LVL ' + str(other.ability_gust.level), 3)
        text.start(SceneManagement.active_scene)
        self.kill()


class OrbSlam(RigidPhysicsAwareGameObject):

    def __init__(self):
        sprite: Surface = ResourceManagement.get_image('orb_slam.png')
        RigidPhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_slam.level_up()
        text = InformationBanner('SLAM UPGRADED !', 'SLAM LVL ' + str(other.ability_slam.level), 3)
        text.start(SceneManagement.active_scene)
        self.kill()
