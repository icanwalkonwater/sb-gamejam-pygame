import time
from abc import ABC, abstractmethod

from pygame.math import Vector2

from constants import EntitySettings


class LivingEntity(ABC):

    def __init__(self, max_health: float, damage_resistance: float = 1, invincibility_duration: float = 0):
        self.health: float = max_health
        self.damage_resistance: float = damage_resistance
        self._invincibility_duration: float = invincibility_duration
        self.__next_hit: float = 0

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    def take_damage(self, damage_points: float):
        if self.__next_hit < time.time():
            self.__next_hit = time.time() + self._invincibility_duration

            self.health -= damage_points * self.damage_resistance
            if self.health <= 0:
                self._die()

    @abstractmethod
    def _die(self):
        pass

    @staticmethod
    def _velocity_to_damage(velocity: Vector2) -> float:
        magnitude = velocity.magnitude_squared()
        if magnitude < EntitySettings.DAMAGE_VELOCITY_THRESHOLD_SQR:
            return 0
        return magnitude * EntitySettings.DAMAGE_VELOCITY_FACTOR_SQR
