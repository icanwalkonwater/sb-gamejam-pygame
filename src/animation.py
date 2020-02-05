import time
from enum import Enum
from math import floor
from typing import List

from pygame.sprite import Sprite
from pygame.surface import Surface


class AnimatedSprite(Sprite):

    def __init__(self, animations: {Enum, List[Surface]}, frequency: float, default_state: Enum):
        Sprite.__init__(self)
        self.animations = animations
        self.frequency = frequency
        self._state = default_state
        self.__sprite_generator = self.__get_current_frame_generator()

    def update(self, delta_time: float):
        self.image = next(self.__sprite_generator)

    def __get_current_frame_generator(self):
        start_time = time.time()
        while True:
            time_offset = time.time() - start_time
            sprite_index = floor(time_offset * self.frequency) \
                           % len(self.animations.get(self._state))

            yield self.animations.get(self._state)[sprite_index]
