from enum import Enum
from os import path
from typing import Dict, List

from pygame import Surface, image, transform

from enums import PlayerState, ButtonState, EnemyState, WindDirection, ProjectileState, TornadoProjectileState


class ResourceManagement:
    __images_cache: Dict[str, Surface] = {}

    @classmethod
    def get_player_sprites(cls) -> {Enum, List[Surface]}:
        return {
            PlayerState.IDLE: [cls.get_image("wizard_idle_1.png"), cls.get_image("wizard_idle_2.png")],
            PlayerState.RUNNING_RIGHT: [cls.get_image("wizard_running_1R.png"),
                                        cls.get_image("wizard_running_2R.png")],
            PlayerState.RUNNING_LEFT: [cls.get_image("wizard_running_1L.png"),
                                       cls.get_image("wizard_running_2L.png")],
            PlayerState.FLYING: [cls.get_image("wizard_flying_1.png"), cls.get_image("wizard_flying_2.png")]
        }

    @classmethod
    def get_environment_button_sprites(cls) -> {Enum, List[Surface]}:
        return {
            ButtonState.ON: [cls.get_image(path.join("props", "button_on.png"))],
            ButtonState.OFF: [cls.get_image(path.join("props", "button_off.png"))]
        }

    @classmethod
    def get_environment_wind_stream_sprites(cls, size: (int, int)) -> {Enum, List[Surface]}:
        sprites = {
            WindDirection.UP: [cls.get_image(path.join("props", "wind_stream_1.png")),
                               cls.get_image(path.join("props", "wind_stream_2.png"))],
            WindDirection.DOWN: [transform.flip(e, False, True) for e in
                                 [cls.get_image(path.join("props", "wind_stream_1.png")),
                                  cls.get_image(path.join("props", "wind_stream_2.png"))]
                                 ],
            WindDirection.LEFT: [transform.rotate(e, -90) for e in
                                 [cls.get_image(path.join("props", "wind_stream_1.png")),
                                  cls.get_image(path.join("props", "wind_stream_2.png"))]
                                 ],
            WindDirection.RIGHT: [transform.rotate(e, 90) for e in
                                  [cls.get_image(path.join("props", "wind_stream_1.png")),
                                   cls.get_image(path.join("props", "wind_stream_2.png"))]
                                  ],

        }
        for key in sprites.keys():
            sprites[key] = [transform.scale(sprite, size) for sprite in sprites.get(key)]
        return sprites

    @classmethod
    def get_enemy_ice_sprites(cls) -> {Enum, List[Surface]}:
        return {
            EnemyState.RUNNING_RIGHT: [transform.flip(i, True, False) for i in
                                       [cls.get_image(path.join("hostiles", "ice_running_1.png")),
                                        cls.get_image(path.join("hostiles", "ice_running_2.png"))]],
            EnemyState.RUNNING_LEFT: [cls.get_image(path.join("hostiles", "ice_running_1.png")),
                                      cls.get_image(path.join("hostiles", "ice_running_2.png"))],
            EnemyState.ATTACKING_RIGHT: [
                transform.flip(cls.get_image(path.join("hostiles", "ice_jumping.png")), True, False)],
            EnemyState.ATTACKING_LEFT: [cls.get_image(path.join("hostiles", "ice_jumping.png"))]
        }

    @classmethod
    def get_enemy_fire_sprites(cls) -> {Enum, List[Surface]}:
        return {
            EnemyState.RUNNING_RIGHT: [transform.flip(i, True, False) for i in
                                       [cls.get_image(path.join("hostiles", "fire_walking_calm_1.png")),
                                        cls.get_image(path.join("hostiles", "fire_walking_calm_2.png"))]],
            EnemyState.RUNNING_LEFT: [cls.get_image(path.join("hostiles", "fire_walking_calm_1.png")),
                                      cls.get_image(path.join("hostiles", "fire_walking_calm_2.png"))],
            EnemyState.ATTACKING_RIGHT: [transform.flip(i, True, False) for i in
                                         [cls.get_image(path.join("hostiles", "fire_walking_angry_1.png")),
                                          cls.get_image(path.join("hostiles", "fire_walking_angry_2.png"))]],
            EnemyState.ATTACKING_LEFT: [cls.get_image(path.join("hostiles", "fire_walking_angry_1.png")),
                                        cls.get_image(path.join("hostiles", "fire_walking_angry_2.png"))],
        }

    @classmethod
    def get_projectile_gust_sprites(cls) -> {Enum, List[Surface]}:
        return {
            ProjectileState.DEFAULT: [cls.get_image(path.join("projectiles", "gust_" + str(i) + ".png")) for i in
                                      range(1, 9)]
        }

    @classmethod
    def get_projectile_slam_sprites(cls, size: (int, int)) -> {Enum, List[Surface]}:
        sprites = {
            ProjectileState.DEFAULT: [cls.get_image(path.join("projectiles", "slam_1.png")),
                                      cls.get_image(path.join("projectiles", "slam_2.png")),
                                      cls.get_image(path.join("projectiles", "slam_3.png"))]
        }
        for key in sprites.keys():
            sprites[key] = [transform.scale(sprite, size) for sprite in sprites.get(key)]
        return sprites

    @classmethod
    def get_projectile_fire_ball_sprites(cls) -> {Enum, List[Surface]}:
        return {
            ProjectileState.DEFAULT: [cls.get_image(path.join("projectiles", "FB00" + str(i) + ".png")) for i in
                                      range(1, 5)]
        }

    @classmethod
    def get_projectile_tornado_sprites(cls) -> {Enum, List[Surface]}:
        return {
            TornadoProjectileState.SMALL: [cls.get_image(path.join("projectiles", "tornado_1_sml.png")),
                                           cls.get_image(path.join("projectiles", "tornado_2_sml.png")), ],
            TornadoProjectileState.BIG: [cls.get_image(path.join("projectiles", "tornado_1_big.png")),
                                         cls.get_image(path.join("projectiles", "tornado_2_big.png")), ]
        }

    @classmethod
    def get_ability_jump_sprite(cls) -> Surface:
        return cls.get_image("ui-ability-jump-button.png")

    @classmethod
    def get_ability_gust_sprite(cls) -> Surface:
        return cls.get_image("ui-ability-gust-button.png")

    @classmethod
    def get_ability_slam_sprite(cls) -> Surface:
        return cls.get_image("ui-ability-slam-button.png")

    @classmethod
    def get_image(cls, image_path: str):
        target_image: Surface = cls.__images_cache.get(image_path)
        if target_image is None:
            target_image: Surface = image.load(path.join('assets', image_path))
            cls.__images_cache[image_path] = target_image.convert_alpha()

        return target_image
