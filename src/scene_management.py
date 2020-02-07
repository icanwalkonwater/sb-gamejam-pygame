import sys
from typing import Dict

import pygame

from scene import Scene


class SceneManagement:
    __scenes: Dict[str, Scene]
    active_scene: Scene

    @classmethod
    def init(cls, scenes: Dict[str, Scene]):
        cls.__scenes = scenes
        cls.active_scene = None

    @classmethod
    def load_scene(cls, name: str):
        new_scene = cls.__scenes.get(name)
        if new_scene == cls.active_scene:
            raise RuntimeError('Can\'t load the same level twice')

        cls.active_scene = new_scene
        if cls.active_scene is None:
            print(f'Unknown scene {name} !')
            sys.exit(1)

        cls.active_scene.draw_init(pygame.display.get_surface())
        cls.active_scene.start()
