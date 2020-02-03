from typing import Tuple

import pygame
from pygame.constants import K_q, K_d, K_z, K_s
from pygame.math import Vector2


class InputController:
    def __init__(self, horizontal: Tuple[int, int] = (K_q, K_d), vertical: Tuple[int, int] = (K_z, K_s),
                 acceleration: Vector2 = Vector2(1, 1)):
        self.horizontal: Tuple[int, int] = horizontal
        self.vertical: Tuple[int, int] = vertical
        self.acceleration: Vector2 = acceleration

    def get_motion(self) -> Vector2:
        motion = Vector2()

        # Trick the event system, otherwise get_pressed() wont return anything
        pygame.event.get(pygame.KEYDOWN)
        pygame.event.clear()

        keys = pygame.key.get_pressed()

        if keys[self.horizontal[0]]:
            motion.x -= self.acceleration.x
        if keys[self.horizontal[1]]:
            motion.x += self.acceleration.x

        if keys[self.vertical[0]]:
            motion.y -= self.acceleration.y
        if keys[self.vertical[1]]:
            motion.y += self.acceleration.y

        return motion
