import sys
from typing import Dict

from pygame.surface import Surface

from scene import Scene


class SceneManagement:
    __scenes: Dict[str, Scene]
    active_scene: Scene

    @classmethod
    def init(cls, scenes: Dict[str, Scene]):
        cls.__scenes = scenes
        cls.active_scene = None

    @classmethod
    def load_scene(cls, name: str, screen: Surface):
        cls.active_scene = cls.__scenes.get(name)
        if cls.active_scene is None:
            print(f'Unknown scene {name} !')
            sys.exit(1)

        cls.active_scene.draw_init(screen)
