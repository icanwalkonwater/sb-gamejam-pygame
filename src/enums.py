from enum import Enum


class Layers(Enum):
    """Layers are used for the collision masks"""

    """Layer containing the rigid environment where we can walk on"""
    ENVIRONMENT = 1
    """Layer containing the player"""
    PLAYER = 2
    """Layer containing the enemies"""
    ENEMY = 3
    """Layer containing the projectiles of any origin"""
    PROJECTILE = 4


class ImpactSide(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class PlayerState(Enum):
    IDLE = 1
    RUNNING_LEFT = 2
    RUNNING_RIGHT = 3
    FLYING = 4


class ButtonState(Enum):
    ON = 1
    OFF = 2
