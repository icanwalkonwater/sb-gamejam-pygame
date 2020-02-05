import math
from abc import ABC

from pygame import Vector2
from pygame.rect import Rect
from pygame.sprite import Group
from pygame.surface import Surface

from constants import PHYSICS_NULLIFY_THRESHOLD, PHYSICS_GRAVITY, PHYSICS_STANDARD_RESISTANCE, ImpactSide, VECTOR2_NULL
from game_object import Moveable, GameObject


class PhysicsReceiver(Moveable, ABC):

    def __init__(self, weight: float, resistance_amount: float = PHYSICS_STANDARD_RESISTANCE,
                 initial_velocity: Vector2 = Vector2()):
        self.velocity: Vector2 = Vector2(initial_velocity)
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
        if self.velocity != VECTOR2_NULL:
            self.move(self.velocity * delta_time, True)


class PhysicsAwareGameObject(GameObject, PhysicsReceiver):

    def __init__(self, surface: Surface, weight: float):
        GameObject.__init__(self, surface)
        PhysicsReceiver.__init__(self, weight)

    def update(self, delta_time: float):
        GameObject.update(self, delta_time)
        PhysicsReceiver.update(self, delta_time)

    def move(self, of: Vector2, physics_scale=False):
        self.is_on_ground = False
        GameObject.move(self, of, physics_scale)


class RigidPhysicsAwareGameObject(PhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, collides_with: [Group] = None):
        PhysicsAwareGameObject.__init__(self, surface, weight)

        self.collision_masks: [Group] = []
        if collides_with is not None:
            self.collision_masks.extend(collides_with)

    def add_to_collision_mask(self, *groups: [Group]):
        self.collision_masks.extend(groups)

    def clear_collision_masks(self):
        self.collision_masks.clear()

    @staticmethod
    def __normalize_angle(angle: float) -> float:
        return angle % 360 - 180

    def update(self, delta_time: float):

        # Quick fix: re-enable gravity if we are still moving (do allow use to fall from edges)
        if self.velocity.x != 0:
            self.is_on_ground = False

        PhysicsAwareGameObject.update(self, delta_time)

        self._compute_collisions()

    @classmethod
    def __collide_game_object(cls, lhs: GameObject, rhs: GameObject) -> bool:
        lhs_rect: Rect = lhs.rect
        lhs_left: float = lhs.transform.x
        lhs_top: float = lhs.transform.y

        rhs_rect: Rect = rhs.rect
        rhs_left: float = rhs.transform.x
        rhs_top: float = rhs.transform.y

        # lhs_left >= rhs_right or lhs_right <= rhs_left
        if lhs_left >= rhs_left + rhs_rect.width or lhs_left + lhs_rect.width <= rhs_left:
            return False

        # lhs_top >= rhs_bottom or lhs_bottom <= rhs_top
        if lhs_top >= rhs_top + rhs_rect.height or lhs_top + lhs_rect.height <= rhs_top:
            return False

        return True

    def _compute_collisions(self):
        layer: Group
        for layer in self.collision_masks:
            other: GameObject
            for other in layer.sprites():
                self_rect = self.rect
                other_rect = other.rect

                if self.__collide_game_object(self, other):
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

    def _on_collide(self, other: GameObject, direction_of_impact: Vector2, impact_side: ImpactSide):
        # print(f'Collided with {other} at {impact_side} (direction: {direction_of_impact}) !')
        if impact_side == ImpactSide.BOTTOM:
            # Assuming the floor is at the bottom, we are on the ground
            self.is_on_ground = True
            # Nullify any vertical velocity (assuming we were falling)
            self.velocity.y = 0
            # Displace object to the top of the other
            self.transform.y = other.rect.top - self.height
            # Mark the rect dirty because we have modified the transform
            self._rect_dirty = True
        elif impact_side == ImpactSide.TOP:
            self.velocity.y = 0
            self.transform.y = other.rect.bottom
            self._rect_dirty = True
        elif impact_side == ImpactSide.LEFT:
            self.velocity.x = 0
            self.transform.x = other.rect.right
            self._rect_dirty = True
        # elif impact_side == ImpactSide.RIGHT:
        else:
            self.velocity.x = 0
            self.transform.x = other.rect.left - self.width
            self._rect_dirty = True
