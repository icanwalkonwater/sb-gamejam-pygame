from os import path
from typing import Dict

from pygame import Surface, image


class RessourceManagement:
    __images_cache: Dict[str, Surface] = {}

    @classmethod
    def get_image(cls, image_path: str):
        target_image: Surface = cls.__images_cache.get(image_path)
        if target_image is None:
            target_image: Surface = image.load(path.join('assets', image_path))
            cls.__images_cache[image_path] = target_image.convert_alpha()

        return target_image
