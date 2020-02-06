from enum import Enum
from os import path
from typing import Dict, List

from pygame import Surface, image

from enums import PlayerState, ButtonState


class ResourceManagement:
    __images_cache: Dict[str, Surface] = {}

    @classmethod
    def get_player_sprites(cls) -> {Enum, List[Surface]}:
        return {
            PlayerState.IDLE: [cls.get_image("wizard_idle_1.png"), cls.get_image("wizard_idle_2.png")],
            PlayerState.RUNNING_RIGHT: [cls.get_image("wizard_running_1R.png"), cls.get_image("wizard_running_2R.png")],
            PlayerState.RUNNING_LEFT: [cls.get_image("wizard_running_1L.png"), cls.get_image("wizard_running_2L.png")],
            PlayerState.FLYING: [cls.get_image("wizard_flying.png")]
        }

    @classmethod
    def get_environment_button_sprites(cls) -> {Enum, List[Surface]}:
        return {
            ButtonState.ON: [cls.get_image("button_on.png")],
            ButtonState.OFF: [cls.get_image("button_off.png")]
        }

    @classmethod
    def get_image(cls, image_path: str):
        target_image: Surface = cls.__images_cache.get(image_path)
        if target_image is None:
            target_image: Surface = image.load(path.join('assets', image_path))
            cls.__images_cache[image_path] = target_image.convert_alpha()

        return target_image
