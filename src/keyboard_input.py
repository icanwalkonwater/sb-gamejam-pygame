from typing import Tuple

import pygame
from pygame.constants import K_q, K_d, K_z, K_s, K_AMPERSAND, K_QUOTEDBL, K_QUOTE
from pygame.event import Event
from pygame.math import Vector2


class InputController:
    acceleration: Vector2
    _horizontal: Tuple[int, int]
    _vertical: Tuple[int, int]
    _powers: Tuple[int, int, int, int]
    __keys_pressed: tuple
    __keys_down: [int]

    @classmethod
    def init(cls, horizontal: Tuple[int, int] = (K_q, K_d), vertical: Tuple[int, int] = (K_z, K_s),
             powers: Tuple[int, int, int, int] = (K_AMPERSAND, 233, K_QUOTEDBL, K_QUOTE),  # 233 is 'é'
             acceleration: Vector2 = Vector2(1, 1)):
        cls._horizontal = horizontal
        cls._vertical = vertical
        cls._powers = powers
        cls.acceleration: Vector2 = acceleration

    @classmethod
    def update(cls):
        cls.__keys_pressed = pygame.key.get_pressed()
        cls.__keys_down = list(map(lambda evt: evt.key, pygame.event.get(pygame.KEYDOWN)))

    @classmethod
    def get_motion(cls) -> Vector2:
        motion = Vector2()

        if cls.__keys_pressed[cls._horizontal[0]]:
            motion.x -= cls.acceleration.x
        if cls.__keys_pressed[cls._horizontal[1]]:
            motion.x += cls.acceleration.x

        if cls.__keys_pressed[cls._vertical[0]]:
            motion.y -= cls.acceleration.y
        if cls.__keys_pressed[cls._vertical[1]]:
            motion.y += cls.acceleration.y

        return motion

    @classmethod
    def get_powers(cls) -> (bool, bool, bool, bool):
        return (
            cls._powers[0] in cls.__keys_down,
            cls._powers[1] in cls.__keys_down,
            cls._powers[2] in cls.__keys_down,
            cls._powers[3] in cls.__keys_down
        )
