import sys
from typing import Dict, Callable

import pygame
from pygame.math import Vector2

from game_objects.entities.player_management import PlayerManagement
from music_manager import MusicManager
from scene import Scene


class SceneManagement:
    __scenes: Dict[str, Callable[..., Scene]]
    active_scene: Scene

    @classmethod
    def init(cls, scenes: Dict[str, Callable[..., Scene]]):
        cls.__scenes = scenes
        cls.active_scene = None

    @classmethod
    def load_scene(cls, name: str):
        new_scene = cls.__scenes.get(name)()
        if new_scene == cls.active_scene:
            raise RuntimeError('Can\'t load the same level twice')

        cls.active_scene = new_scene
        if cls.active_scene is None:
            print(f'Unknown scene {name} !')
            sys.exit(1)

        player = PlayerManagement.player
        player.transform = cls.active_scene.player.sprite.transform
        player.velocity = Vector2(0, 0)
        player._rect_dirty = True
        player.kill()
        cls.active_scene.player.add(player)
        cls.active_scene.dynamics.add(player)

        cls.active_scene.draw_init(pygame.display.get_surface())
        cls.active_scene.start()

        MusicManager.stop_music()
        MusicManager.play_music()
