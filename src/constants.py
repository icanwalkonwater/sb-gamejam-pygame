from pygame import Vector2

"""The null Vector2"""
VECTOR2_NULL = Vector2(0, 0)


class GlobalSettings:
    """Screen resolution"""
    RESOLUTION = (1024, 768)


class PhysicsSettings:
    """Physics operate on a higher scale than the transform.
    This is the factor to translate the physics values to the coordinate system.
    """
    SCALE = 10_000

    """If a component of a velocity drop below this threshold, it is set to zero.
    This is to prevent objects from sliding endlessly.
    """
    NULLIFY_THRESHOLD = 1

    """Force applied to every velocity.
    Will be applied differently based on the weight of the object.
    """
    GRAVITY = Vector2(0, 9.31)

    """Used to simulate the decay of the velocity due to the air."""
    STANDARD_RESISTANCE = 0.06


class PlayerSettings:
    """TO REPLACE WITH ABILITY.
    The force to apply when the player want to jump.
    """
    PLAYER_JUMP_FORCE = Vector2(0, -4_500)

    """Factor to apply to the impact direction on collision with an enemy."""
    DAMAGE_REPULSION_FACTOR = -1_000

    """Maximum amount of mana"""
    MANA_MAX = 900

    """Factor used to passively replenish mana when moving around"""
    MANA_PASSIVE_REGENERATION_FACTOR = .00001

    """Maximum health"""
    HEALTH_MAX = 100

    class Ability:
        BASE_LEVEL = 1
        BASE_COOLDOWN = .2

        class TornadoJump:
            COOLDOWN = .2
            STRENGTH = -6_000
            MANA_COST = 50
            TIME_TO_LIVE = 1
            KNOCKBACK_STRENGTH = 400

        class Gust:
            STRENGTH = 20_000
            KNOCKBACK_STRENGTH = -2_000
            PROJECTILE_HIT_STRENGTH_Y = -2_000
            MANA_COST = 30
            TIME_TO_LIVE = .7

        class Slam:
            STRENGTH = -8_000
            AREA_SIZE = (200, 100)
            AREA_TIME_TO_LIVE = 1
            MANA_COST = 70


class EntitySettings:
    """Used when calculating damage relative to velocity (when hitting a wall real fast).
    If the squared magnitude of the velocity of the moving object when hitting a wall is over this threshold,
    it will start receiving damages."""
    DAMAGE_VELOCITY_THRESHOLD_SQR = 5_000 ** 2

    """When hitting a wall, the damage that the entity will take will be the squared magnitude of its velocity
    times this factor."""
    DAMAGE_VELOCITY_FACTOR_SQR = .001


class EnemySettings:
    """Enemy walking velocity.
        When not attacking a player, they will walk according to this velocity.
        """
    CHILL_WALK_VELOCITY = Vector2(.1, 0)

    """A rect centered on the enemy. If the player enter this rect, the enemy
    will start attacking him.
    """
    DETECTION_RANGE_SQR = 150 ** 2

    class HandToHand:
        """Health of the enemy"""
        HEALTH_MAX = 200

        """Cooldown between attacks"""
        ATTACK_COOLDOWN_S = .5

        """Minimum y of the normalized direction of attack.
        Give the effect that the enemy is jumping on the player.
        """
        ATTACK_MIN_JUMP = .5

        """Factor that will be applied to the normalized direction of attack."""
        ATTACK_FACTOR = 3_000

        """Past this velocity, no more force will be applied to attack the player.
        To avoid accelerating indefinitely when attacking.
        """
        ATTACK_VELOCITY_X_MAX = 10_000

        """Distance to the player at which the enemy will start to retreat to avoid glitching in a wall."""
        RETREAT_DISTANCE_SQR = 40 ** 2

        """Force to apply when the enemy need to retreat."""
        RETREAT_FORCE = -500