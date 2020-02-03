import math
from abc import ABC
from enum import Enum

from pygame import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from game_object import Moveable, GameObject

PHYSICS_NULLIFY_THRESHOLD = 1
PHYSICS_GRAVITY = Vector2(0, 9.31)
PHYSICS_STANDARD_RESISTANCE = 0.06


class ImpactSide(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class PhysicsReceiver(Moveable, ABC):

    def __init__(self, weight: float, resistance_amount: float = PHYSICS_STANDARD_RESISTANCE,
                 initial_velocity: Vector2 = Vector2()):
        self.velocity: Vector2 = initial_velocity
        self.resistance_amount: float = resistance_amount
        self.weight = weight
        self.is_on_ground = False

    def apply_force(self, force: Vector2):
        self.velocity += force

    def update_velocity(self, delta_time: float):
        if self.velocity.length_squared() > 0:
            self.velocity.x -= (1 if self.velocity.x > 0 else -1) \
                               * math.sqrt(abs(self.velocity.x)) * self.resistance_amount * delta_time
            self.velocity.y -= (1 if self.velocity.y > 0 else -1) \
                               * math.sqrt(abs(self.velocity.y)) * self.resistance_amount * delta_time

            if 0 < self.velocity.x < PHYSICS_NULLIFY_THRESHOLD:
                self.velocity.x = 0

            if 0 < self.velocity.y < PHYSICS_NULLIFY_THRESHOLD:
                self.velocity.y = 0

    def apply_gravity(self, delta_time: float):
        if not self.is_on_ground:
            self.apply_force(PHYSICS_GRAVITY * self.weight * delta_time)

    def update(self, delta_time: float):
        # print(f'\rVelocity: {self.velocity}', end='')

        self.apply_gravity(delta_time)
        self.update_velocity(delta_time)
        self.move(self.velocity * delta_time, True)


class PhysicsAwareGameObject(GameObject, PhysicsReceiver):

    def __init__(self, surface: Surface, weight: float):
        GameObject.__init__(self, surface)
        PhysicsReceiver.__init__(self, weight)

    def update(self, delta_time: float):
        GameObject.update(self, delta_time)
        PhysicsReceiver.update(self, delta_time)


class RigidPhysicsAwareGameObject(PhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, collides_with: [GameObject] = None):
        PhysicsAwareGameObject.__init__(self, surface, weight)

        self.collision_mask: Group = Group()
        if collides_with is not None:
            self.collision_mask.add(*collides_with)

    def add_to_collision_mask(self, *colliders: [GameObject]):
        self.collision_mask.add(colliders)

    @staticmethod
    def __normalize_angle(angle: float) -> float:
        return angle % 360 - 180

    def update(self, delta_time: float):

        # Quick fix: re-enable gravity if we are still moving (do allow use to fall from edges)
        if self.velocity.x != 0:
            self.is_on_ground = False

        PhysicsAwareGameObject.update(self, delta_time)

        self._compute_collisions()

    def _compute_collisions(self):
        other: GameObject
        for other in self.collision_mask.sprites():
            self_rect = self.rect
            other_rect = other.rect

            if self_rect.colliderect(other_rect):
                direction_of_impact: Vector2 = Vector2(other_rect.center) - Vector2(self_rect.center)

                direction_top_left_corner: Vector2 = Vector2(
                    other_rect.left - other_rect.centerx,
                    other_rect.top - other_rect.centery
                )

                direction_top_right_corner: Vector2 = Vector2(
                    other_rect.right - other_rect.centerx,
                    other_rect.top - other_rect.centery
                )

                angle_delta_vertical = abs(direction_top_left_corner.angle_to(Vector2(0, -1)))
                angle_delta_horizontal = abs(direction_top_right_corner.angle_to(Vector2(1, 0)))

                if -angle_delta_vertical < self.__normalize_angle(
                        direction_of_impact.angle_to(-Vector2(0, -1))) < angle_delta_vertical:
                    self._on_collide(other, direction_of_impact, ImpactSide.TOP)

                elif -angle_delta_vertical < self.__normalize_angle(
                        direction_of_impact.angle_to(-Vector2(0, 1))) < angle_delta_vertical:
                    self._on_collide(other, direction_of_impact, ImpactSide.BOTTOM)

                elif -angle_delta_horizontal < self.__normalize_angle(
                        direction_of_impact.angle_to(-Vector2(-1, 0))) < angle_delta_horizontal:
                    self._on_collide(other, direction_of_impact, ImpactSide.LEFT)

                # elif -angle_delta_horizontal < self.__normalize_angle(
                #       direction_of_impact.angle_to(-Vector2(1, 0))) < angle_delta_horizontal:
                else:
                    self._on_collide(other, direction_of_impact, ImpactSide.RIGHT)

                # print(f'Not normalized: {direction_of_impact} ', end='')
                # direction_of_impact.normalize_ip()
                #
                # print(f", normalized: {direction_of_impact}", end='')
                # ratio_to_edge = max(
                #     abs(direction_of_impact.x) / (self_rect.width / 2),
                #     abs(direction_of_impact.y) / (self_rect.height / 2)
                # )
                # direction_of_impact *= 1 / ratio_to_edge
                #
                # print(f", scaled: {direction_of_impact}")
                #
                # print(self_rect.width)
                #
                # local_impact_point = (
                #     direction_of_impact.x * (self_rect.width / 2),
                #     direction_of_impact.y * (self_rect.height / 2)
                # )
                #
                # self._on_collide(other, direction_of_impact, local_impact_point)

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        # print(f'Collided with {other} at {impact_side} (direction: {direction_of_impact}) !')
        if impact_side == ImpactSide.BOTTOM:
            self.is_on_ground = True
            self.velocity.y = 0
            self.transform.y = other.rect.top - self.height
        elif impact_side == ImpactSide.TOP:
            self.velocity.y = 0
            self.transform.y = other.rect.bottom
        elif impact_side == ImpactSide.LEFT:
            self.velocity.x = 0
            self.transform.x = other.rect.right
        # elif impact_side == ImpactSide.RIGHT:
        else:
            self.velocity.x = 0
            self.transform.x = other.rect.left - self.width
