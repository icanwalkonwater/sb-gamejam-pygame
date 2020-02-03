import math
import time

import pygame
from pygame.surface import Surface


class Effect:
    def __init__(self):
        pass

    def apply(self, surface:Surface) -> Surface:
        pass

    def applicable(self) -> bool:
        pass

class WizEffect(Effect):
    def create_displacement(self):
        start_time = time.time()
        percent = 0

        while percent < 1:
            percent = (time.time() - start_time) / self.duration
            displacement_x = math.sin(percent * self.frequency)
            if displacement_x > 0:
                displacement_x = 1
            else:
                displacement_x = -1
            displacement_x = displacement_x * self.scale

            displacement_y = math.cos(percent * self.frequency)
            if displacement_y > 0:
                displacement_y = 1
            else:
                displacement_y = -1
            displacement_y = displacement_y * self.scale
            yield int(displacement_x), int(displacement_y)

    def __init__(self, scale: int, frequency: float, duration: float):
        self.scale = scale
        self.frequency = frequency
        self.duration = duration
        self.__displacements_generator = None

    def apply(self, surface: Surface) -> Surface:
        if self.__displacements_generator:
            try:
                displacement = next(self.__displacements_generator)
            except StopIteration :
                displacement = None
            if displacement:
                surface.scroll(displacement[0], displacement[1])
            else:
                self.__displacements_generator = None
        return surface

    def start(self):
        self.__displacements_generator = self.create_displacement()

    def applicable(self) -> bool:
        return self.__displacements_generator
