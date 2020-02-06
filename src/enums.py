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

    @classmethod
    def from_name(cls, name) -> Enum:
        if name == 'environment':
            return cls.ENVIRONMENT
        elif name == 'player':
            return cls.PLAYER
        elif name == 'enemy':
            return cls.ENEMY
        elif name == 'projectile':
            return cls.PROJECTILE
        else:
            raise TypeError(f'No layer with the name : {name}')


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


class WindDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class ProjectileState(Enum):
    DEFAULT = 0


class EnemyState(Enum):
    RUNNING_RIGHT = 1
    RUNNING_LEFT = 2
    ATTACKING_RIGHT = 3
    ATTACKING_LEFT = 4


class TornadoProjectileState:
    SMALL = 1
    BIG = 2
