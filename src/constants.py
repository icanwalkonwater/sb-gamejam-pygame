from enum import Enum

from pygame import Vector2

"""Screen resolution"""
RESOLUTION = (1024, 768)

"""Physics operate on a higher scale than the transform.
This is the factor to translate the physics values to the coordinate system.
"""
PHYSICS_SCALE = 10000
"""If a component of a velocity drop below this threshold, it is set to zero.
This is to prevent objects from sliding endlessly.
"""
PHYSICS_NULLIFY_THRESHOLD = 1
"""Force applied to every velocity.
Will be applied differently based on the weight of the object.
"""
PHYSICS_GRAVITY = Vector2(0, 9.31)
"""Used to simulate the decay of the velocity due to the air."""
PHYSICS_STANDARD_RESISTANCE = 0.06

"""TO REPLACE WITH ABILITY.
The force to apply when the player want to jump.
"""
PLAYER_JUMP_FORCE = Vector2(0, -4_500)
"""Factor to apply to the impact direction on collision with an enemy."""
PLAYER_DAMAGE_REPULSION_FACTOR = -1000

"""Enemy walking velocity.
When not attacking a player, they will walk according to this velocity.
"""
ENEMY_CHILL_WALK_VELOCITY = Vector2(1_000, 0)
"""A rect centered on the enemy. If the player enter this rect, the enemy
will start attacking him.
"""
ENEMY_DETECTION_RANGE_SQR = 150 ** 2

# Hand to hand enemy
"""Cooldown between attacks"""
ENEMY_HTH_ATTACK_COOLDOWN = .5
"""Minimum y of the normalized direction of attack.
Give the effect that the enemy is jumping on the player.
"""
ENEMY_HTH_ATTACK_MIN_JUMP = .5
"""Factor that will be applied to the normalized direction of attack."""
ENEMY_HTH_ATTACK_FACTOR = 3_000
"""Past this velocity, no more force will be applied to attack the player.
To avoid accelerating indefinitely when attacking.
"""
ENEMY_HTH_ATTACK_VELOCITY_X_MAX = 10_000
"""Distance to the player at which the enemy will start to retreat to avoid glitching in a wall."""
ENEMY_HTH_RETREAT_DISTANCE_SQR = 50 ** 2
"""Force to apply when the enemy need to retreat."""
ENEMY_HTH_RETREAT_FORCE = -2000

PLAYER_MANA_MAX = 900
PLAYER_MANA_WALK_REGENERATION_FACTOR = .00001

PLAYER_ABILITY_BASE_LEVEL = 1
PLAYER_ABILITY_BASE_COOLDOWN = .2

PLAYER_ABILITY_TORNADO_JUMP_COOLDOWN = .2
PLAYER_ABILITY_TORNADO_JUMP_STRENGTH = -6000
PLAYER_ABILITY_TORNADO_JUMP_BASE_MANA_COST = 50

PLAYER_ABILITY_GUST_BASE_STRENGTH = 20000
PLAYER_ABILITY_GUST_BASE_KNOCKBACK_STRENGTH = -2000
PLAYER_ABILITY_GUST_UPWARD_STRENGTH = -2000
PLAYER_ABILITY_GUST_BASE_MANA_COST = 30

PLAYER_ABILITY_SLAM_BASE_STRENGTH = -8000
PLAYER_ABILITY_SLAM_BASE_AREA = 200
PLAYER_ABILITY_SLAM_HEIGHT = 5
PLAYER_ABILITY_SLAM_WIDTH = 200
PLAYER_ABILITY_SLAM_TIME_TO_LIVE = 1
PLAYER_ABILITY_SLAM_BASE_MANA_COST = 70


class Layers(Enum):
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
