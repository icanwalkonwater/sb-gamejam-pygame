from pygame import surface, Surface, Vector2

from entities.player import Player
from enums import PowerOrb, ImpactSide
from game_object import GameObject
from physics import PhysicsAwareGameObject
from scene import Scene


class Orb(PhysicsAwareGameObject):
    def __init__(self, power: PowerOrb):
        PhysicsAwareGameObject.__init__(self, Orb._surface_creator(power), 0)
        self.power = power

    @staticmethod
    def _surface_creator(power: PowerOrb) -> Surface:
        sprite: Surface = Surface((20, 20))
        if power == PowerOrb.GUST:
            sprite.fill((255, 50, 50))
        if power == PowerOrb.SLAM:
            sprite.fill((50, 255, 50))
        if power == PowerOrb.TORNADO_JUMP:
            sprite.fill((50, 50, 255))
        return sprite

    def start(self, scene: Scene):
        self.add_to_collision_mask(scene.player)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide, delta_time: float):
        other: Player

        if self.power == PowerOrb.GUST:
            other.ability_gust.level_up()
        if self.power == PowerOrb.SLAM:
            other.ability_slam.level_up()
        if self.power == PowerOrb.TORNADO_JUMP:
            other.ability_tornado_jump.level_up()
        #Todo Pop Up

        self.kill()
