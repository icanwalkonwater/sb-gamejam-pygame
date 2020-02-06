import time
from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from game_objects.entities.player import Player
from game_objects.game_object import GameObject
from ressource_management import ResourceManagement
from scene import Scene


class UIIndicator(GameObject, ABC):

    def __init__(self, surface: Surface, position: (int, int)):
        GameObject.__init__(self, surface)
        # Save sprite
        self._original_image = surface
        self._disabled_image = surface.copy()
        self._disabled_image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

        self.move(Vector2(position[0], position[1]))
        self._player: Player = None

    def start(self, scene: Scene):
        self._player = scene.player.sprite

    def update(self, delta_time: float):
        self.image = self._original_image if self._is_enabled() else self._disabled_image

    @abstractmethod
    def _is_enabled(self):
        pass


class UITornadoJumpIndicator(UIIndicator):

    def __init__(self):
        UIIndicator.__init__(self, ResourceManagement.get_ability_jump_sprite(), (10, 163))

    def _is_enabled(self):
        return self._player.ability_tornado_jump._next_usage <= time.time()


class UIGustIndicator(UIIndicator):

    def __init__(self):
        UIIndicator.__init__(self, ResourceManagement.get_ability_gust_sprite(), (10, 230))

    def _is_enabled(self):
        return self._player.ability_gust._next_usage <= time.time()


class UISlamIndicator(UIIndicator):

    def __init__(self):
        UIIndicator.__init__(self, ResourceManagement.get_ability_slam_sprite(), (10, 296))

    def _is_enabled(self):
        return self._player.ability_slam._next_usage <= time.time()
