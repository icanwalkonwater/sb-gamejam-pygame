from pygame import Surface, Vector2

from entities.player import Player
from enums import ImpactSide
from game_object import GameObject
from physics import PhysicsAwareGameObject
from scene import Scene


class OrbTornado(PhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((255, 50, 50))
        PhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_tornado_jump.level_up()
        self.kill()


class OrbGust(PhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((50, 255, 50))
        PhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_gust.level_up()
        self.kill()


class OrbSlam(PhysicsAwareGameObject):
    def __init__(self):
        sprite: Surface = Surface((20, 20))
        sprite.fill((50, 50, 255))
        PhysicsAwareGameObject.__init__(self, sprite, 0)

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player
        other.ability_slam.level_up()
        self.kill()
