from typing import Callable, Dict
from xml.etree import ElementTree as ET

from pygame.math import Vector2
from pygame.surface import Surface

from entities.hostiles.heavy_rock_enemy import HeavyRockEnemy
from constants import VECTOR2_NULL
from entities.hostiles.hth_enemy import HthEnemy
from entities.hostiles.ranged_enemy import RangedEnemy
from entities.orb import OrbTornado, OrbGust, OrbSlam
from entities.player import Player
from enums import Layers
from environement_props import ButtonGameObject
from game_object import GameObject
from physics import RigidPhysicsAwareGameObject
from ressource_management import ResourceManagement
from scene import Scene
from ui.abilities_indicators import UITornadoJumpIndicator, UIGustIndicator, UISlamIndicator
from ui.player_bar import UIHealthBar, UIManaBar


class SceneLoader:

    def __init__(self, filename: str, button_bindings: {str, Callable} = None):
        tree: ET.ElementTree = ET.parse(filename)
        self.root: ET.Element = tree.getroot()
        self._button_bindings: Dict[str, Callable] = button_bindings if button_bindings is not None else {}
        self._global_offset = VECTOR2_NULL

    def parse_all(self):
        scene: Scene = Scene(self.__parse_background(), [], [], [])
        self.__parse_global_offset()

        statics = self.__parse_go_list(scene, self.root.find('statics'))
        dynamics = self.__parse_go_list(scene, self.root.find('dynamics'))

        # Reset global offset for the UI
        self._global_offset = VECTOR2_NULL
        ui = self.__parse_go_list(scene, self.root.find('ui'))

        scene.statics.add(*statics)
        scene.dynamics.add(*dynamics)
        scene.ui.add(*ui)

        return scene

    def __parse_background(self) -> Surface:
        element: ET.Element = self.root.find('background')
        if element.attrib['color']:
            surface: Surface = Surface(self.__parse_dimensions(element))
            surface.fill(self.__parse_color(element))
            return surface
        else:
            return ResourceManagement.get_image(element.attrib['src'])

    def __parse_global_offset(self) -> Vector2:
        element: ET.Element = self.root.find('global-offset')
        if element is not None:
            x, y, *_ = self.__parse_transform(element)
            self._global_offset = Vector2(x, y)

    def __parse_go_list(self, scene: Scene, elements: [ET.Element]) -> [GameObject]:
        gos = []
        element: ET.Element
        for element in elements:
            if element.tag == 'box':
                go = self.__parse_box(element)
            elif element.tag == 'rigid-box':
                go = self.__parse_rigid_box(scene, element)
            elif element.tag == 'player':
                go = self.__parse_player(scene, element)
            elif element.tag == 'enemy-hth':
                go = self.__parse_enemy_hth(scene, element)
            elif element.tag == 'enemy-ranged':
                go = self.__parse_enemy_ranged(scene, element)
            elif element.tag == 'enemy-heavy-rock':
                go = self.__parse_enemy_heavy_rock(scene, element)
            elif element.tag == 'prop-button':
                go = self.__parse_prop_button(element)
            elif element.tag == 'orb-tornado':
                go = self.__parse_orb_tornado()
            elif element.tag == 'ui-player-health':
                go = UIHealthBar()
            elif element.tag == 'ui-player-mana':
                go = UIManaBar()
            elif element.tag == 'ui-ability-jump':
                go = UITornadoJumpIndicator()
            elif element.tag == 'ui-ability-gust':
                go = UIGustIndicator()
            elif element.tag == 'ui-ability-slam':
                go = UISlamIndicator()
            else:
                go = None

            if go:
                self.__assign_additional_layers(scene, element, go)
                gos.append(go)

        return gos

    def __parse_box(self, element: ET.Element) -> GameObject:
        if 'src' in element.attrib:
            surface: Surface = ResourceManagement.get_image(element.attrib['src'])
        else:
            surface: Surface = Surface(self.__parse_dimensions(element))
            surface.fill(self.__parse_color(element))

        go = GameObject(surface)
        self.__assign_transform(element, go)

        return go

    @classmethod
    def __parse_rigid_box(cls, scene: Scene, element: ET.Element) -> GameObject:
        if element.attrib['color']:
            surface: Surface = Surface(cls.__parse_dimensions(element))
            surface.fill(cls.__parse_color(element))

            if element.attrib['weight']:
                weight = float(element.attrib['weight'])
            else:
                weight = 0

            go = RigidPhysicsAwareGameObject(surface, weight)
            cls.__assign_transform(element, go)
            cls.__assign_collision_masks(scene, go, cls.__parse_collision_mask(element))

            return go
        else:
            raise RuntimeError('no color on rigid box')

    def __parse_player(self, scene: Scene, element: ET.Element) -> Player:
        player = Player()
        self.__assign_transform(element, player)
        self.__assign_collision_masks(scene, player, self.__parse_collision_mask(element))

        return player

    def __parse_enemy_hth(self, scene: Scene, element: ET.Element) -> HthEnemy:
        enemy = HthEnemy()
        self.__assign_transform(element, enemy)
        self.__assign_collision_masks(scene, enemy, self.__parse_collision_mask(element))

        return enemy

    def __parse_enemy_heavy_rock(self, scene: Scene, element: ET.Element) -> HeavyRockEnemy:
        enemy = HeavyRockEnemy()
        self.__assign_transform(element, enemy)
        self.__assign_collision_masks(scene, enemy, self.__parse_collision_mask(element))

        return enemy

    def __parse_enemy_ranged(self, scene: Scene, element: ET.Element) -> RangedEnemy:
        enemy = RangedEnemy()
        self.__assign_transform(element, enemy)
        self.__assign_collision_masks(scene, enemy, self.__parse_collision_mask(element))

        return enemy

    def __parse_orb_tornado(self, scene: Scene, element: ET.Element) -> OrbTornado:
        orb = OrbTornado
        self.__assign_transform(element, orb)
        self.__assign_collision_masks(scene, orb, self.__parse_collision_mask(element))

        return orb

    def __parse_orb_gust(self, scene: Scene, element: ET.Element) -> OrbGust:
        orb = OrbGust()
        self.__assign_transform(element, orb)
        self.__assign_collision_masks(scene, orb, self.__parse_collision_mask(element))

        return orb

    def __parse_orb_slam(self, scene: Scene, element: ET.Element) -> OrbSlam:
        orb = OrbSlam()
        self.__assign_transform(element, orb)
        self.__assign_collision_masks(scene, orb, self.__parse_collision_mask(element))

        return orb

    def __parse_prop_button(self, element: ET.Element):
        button = ButtonGameObject()
        self.__assign_transform(element, button)

        button_id: str = element.attrib['id']
        if button_id in self._button_bindings:
            self._button_bindings.get(button_id)(button)

        return button

    def __assign_transform(self, element: ET.Element, go: GameObject):
        (x, y, center) = self.__parse_transform(element.find('transform'))
        if center:
            go.center = Vector2(x, y)
        else:
            go.transform = Vector2(x, y)

        go.move(self._global_offset)

    @staticmethod
    def __assign_collision_masks(scene: Scene, go: RigidPhysicsAwareGameObject, layers: [Layers]):
        for layer in layers:
            go.add_to_collision_mask(scene.layers.get(layer))

    @classmethod
    def __assign_additional_layers(cls, scene: Scene, element: ET.Element, go: GameObject):
        if 'additional-layers' in element.attrib:
            for layer_name in element.attrib['additional-layers'].split(','):
                # noinspection PyTypeChecker
                layer: Layers = Layers.from_name(layer_name)
                scene.layers.get(layer).add(go)

    @staticmethod
    def __parse_collision_mask(element: ET.Element) -> [Layers]:
        collision_mask_el = element.find('collision-mask')
        if collision_mask_el is not None:
            return [Layers.from_name(layer_el.text) for layer_el in collision_mask_el.findall('layer')]
        else:
            return []

    @staticmethod
    def __parse_color(element: ET.Element, default: (int, int, int) = (0, 0, 0)) -> (int, int, int):
        if element.attrib['color']:
            return tuple([int(c) for c in element.attrib['color'].split(',')])
        else:
            return default

    @staticmethod
    def __parse_dimensions(element: ET.Element, defaults: (int, int) = (0, 0)) -> (int, int):
        width = int(element.attrib.get('width', defaults[0]))
        height = int(element.attrib.get('height', defaults[1]))

        return width, height

    @staticmethod
    def __parse_transform(element: ET.Element) -> (int, int, bool):
        x = float(element.attrib.get('x', 0))
        y = float(element.attrib.get('y', 0))

        return x, y, 'center' in element.attrib
