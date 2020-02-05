import time
from enum import Enum
from math import floor
from typing import Dict, List

from pygame.sprite import Sprite

from ressource_management import RessourceManagement


class AnimatedSprite(Sprite):

    def __init__(self, animations: Dict[Enum, List[str]], frequency: float, default_state: Enum):
        Sprite.__init__(self)
        self.animations = animations
        self.animation_frequency = frequency
        self._state = default_state
        self.animation_sprite_generator = self.__get_current_frame()

    def update(self, delta_time: float):
        self.image = next(self.animation_sprite_generator)

    def __get_current_frame(self):
        start_time = time.time()
        while True:
            duration = time.time() - start_time
            sprite_index = floor(duration * self.animation_frequency) % len(
                self.animations.get(self._state))
            yield RessourceManagement.get_image(self.animations.get(self._state)[sprite_index])
