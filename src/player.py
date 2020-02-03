from pygame import Vector2, Surface

from game_object import GameObject
from keyboard_input import InputController
from physics import RigidPhysicsAwareGameObject

JUMP_FORCE = Vector2(0, -4500)


class Player(RigidPhysicsAwareGameObject):

    def __init__(self, surface: Surface, weight: float, collides_with: [GameObject] = [],
                 input_controller: InputController = None):
        RigidPhysicsAwareGameObject.__init__(self, surface, weight, collides_with)
        self._input_controller: InputController = input_controller

    def update(self, delta_time: float):
        RigidPhysicsAwareGameObject.update(self, delta_time)

        motion = self._input_controller.get_motion() * delta_time

        if motion.x != 0:
            self.apply_force(Vector2(motion.x, 0))

        if motion.y < 0 and self.is_on_ground:
            self.jump()

    def jump(self):
        self.is_on_ground = False
        self.apply_force(JUMP_FORCE)
