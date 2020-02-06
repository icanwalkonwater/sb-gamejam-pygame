import time
from enum import Enum
from math import floor
from typing import List, Generator, Dict

from pygame.sprite import Sprite
from pygame.surface import Surface


class AnimatedSprite(Sprite):

    def __init__(self, animations: Dict[Enum, List[Surface]], frequency: float, default_state: Enum):
        Sprite.__init__(self)
        # self.image = next(iter(animations.values()))  # Assign the image to the first value we find in the animations
        self.animations: {Enum, List[Surface]} = animations
        self.frequency: float = frequency
        self._state: Enum = default_state
        self.__sprite_generator: Generator = self.__get_current_frame_generator()

    def update(self, delta_time: float):
        self.image = next(self.__sprite_generator)

    def __get_current_frame_generator(self):
        start_time = time.time()
        while True:
            time_offset = time.time() - start_time
            sprite_index = floor(time_offset * self.frequency) \
                           % len(self.animations.get(self._state))

            yield self.animations.get(self._state)[sprite_index]
