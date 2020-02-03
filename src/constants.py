from enum import Enum

from pygame import Vector2
from pygame.rect import Rect

RESOLUTION = (1024, 768)

PHYSICS_SCALE = 10000
PHYSICS_NULLIFY_THRESHOLD = 1
PHYSICS_GRAVITY = Vector2(0, 9.31)
PHYSICS_STANDARD_RESISTANCE = 0.06

PLAYER_JUMP_FORCE = Vector2(0, -4500)

ENEMY_CHILL_WALK_VELOCITY = Vector2(1000, 0)
ENEMY_DETECTION_RANGE = Rect((0, 0), (300, 300))


class ImpactSide(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
