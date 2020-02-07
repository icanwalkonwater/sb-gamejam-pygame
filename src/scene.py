from typing import List, Callable, Dict

from pygame import Surface, Rect
from pygame.math import Vector2
from pygame.sprite import Group, RenderUpdates, GroupSingle, Sprite

from constants import GlobalSettings
from enums import Layers
from game_objects.game_object import GameObject


class ScrollGroup(RenderUpdates):

    def __init__(self, dimensions: (int, int), *args, **kwargs):
        RenderUpdates.__init__(self, *args, **kwargs)
        self.state: Rect = Rect((100, 0), dimensions)

    def center(self, what: Vector2) -> bool:
        casted = (int(what.x), int(what.y))
        if self.state.center == casted:
            return False
        else:
            self.state.center = casted
            return True

    def draw(self, surface: Surface):
        sprite_dict: {Sprite, Rect} = self.spritedict
        surface_blit: Callable = surface.blit
        invalidated: [Rect] = self.lostsprites
        self.lostsprites = []
        invalidated_append: Callable = invalidated.append

        sprite: Sprite
        for sprite in self.sprites():
            sprite.image: Surface
            sprite.rect: Rect

            previous_blit: Rect = sprite_dict[sprite]
            new_blit: Rect = surface_blit(sprite.image, sprite.rect.move(-self.state.left, -self.state.top))
            if previous_blit:
                if new_blit.colliderect(previous_blit):
                    invalidated_append(new_blit.union(previous_blit))
                else:
                    invalidated_append(new_blit)
                    invalidated_append(previous_blit)
            else:
                invalidated_append(new_blit)
            sprite_dict[sprite] = new_blit

        return invalidated

    def __draw(self, surface: Surface):
        # Taken from the original draw() method of RenderUpdates
        # but tweaked to incorporate scrolling
        sprite_dict: {Sprite, Rect} = self.spritedict
        surface_blit: Callable = surface.blit
        dirty: [Rect] = self.lostsprites
        self.lostsprites: [Rect] = []
        dirty_append: Callable = dirty.append

        sprite: Sprite
        for sprite in self.sprites():
            sprite.image: Surface
            sprite.rect: Rect
            current_rect: Rect = sprite_dict[sprite]
            # Blit with offset relative to the 'camera' position
            new_rect: Rect = surface_blit(sprite.image, sprite.rect.move(-self.state.left, -self.state.top))
            if current_rect:
                if new_rect.colliderect(current_rect):
                    dirty_append(new_rect.union(current_rect))
                else:
                    dirty_append(new_rect)
                    dirty_append(current_rect)
            else:
                dirty_append(new_rect)
            sprite_dict[sprite] = new_rect

        return dirty

    def __clear(self, surface: Surface, bgd: Surface):
        # Taken from the original clear method but tweaked to apply scrolling
        surface_blit = surface.blit
        displacement: (int, int) = (-self.state.left, -self.state.top)
        rect: Rect
        for rect in self.lostsprites:
            surface_blit(bgd, rect, rect.move(-self.state.left, -self.state.top))
        rect: Rect
        for rect in self.spritedict.values():
            if rect:
                surface_blit(bgd, rect, rect.move(-self.state.left, -self.state.top))


class Scene:

    def __init__(self, background: Surface, statics: [GameObject], dynamics: [GameObject], ui: [GameObject]):
        self.background: Surface = background
        # Cached background with every statics blighted on it
        self.__background: Surface = None

        # Objects that are not supposed to move and that will be blited onto the background only once
        # but will still receive update()
        self.statics: Group = Group(statics)
        # Objects that will change appearance in some way and will be rendered individually
        self.dynamics: ScrollGroup = ScrollGroup(GlobalSettings.RESOLUTION, dynamics)
        # Objects that are not supposed to live in world space but in camera space
        self.ui: RenderUpdates = RenderUpdates(ui)

        # Layers used for collision masks
        self.layers: Dict[Layers, Group] = {
            Layers.ENVIRONMENT: Group(),
            Layers.PLAYER: GroupSingle(),
            Layers.ENEMY: Group(),
            Layers.PROJECTILE: Group()
        }

        self.__state_dirty: bool = True

    @property
    def environment(self) -> Group:
        return self.layers[Layers.ENVIRONMENT]

    @property
    def player(self) -> GroupSingle:
        return self.layers[Layers.PLAYER]

    @property
    def enemies(self) -> Group:
        return self.layers[Layers.ENEMY]

    @property
    def projectiles(self) -> Group:
        return self.layers[Layers.PROJECTILE]

    def draw_init(self, surface: Surface):
        # Reset background
        self.__background: Surface = self.background.copy()
        # Blit statics onto background
        self.__background.blits(
            ((go.image, go.rect) for go in self.statics.sprites())
        )

        self.draw_statics(surface)

    def draw_auto(self, surface: Surface):
        invalidated = []
        # Clear the dynamic objects
        # if not self.__state_dirty:
        #     self.dynamics.clear(surface, self.__background)
        # else:
        #     self.draw_statics(surface)
        #     invalidated.append(self.__background.get_rect())
        #     self.__state_dirty = False
        self.draw_statics(surface)
        invalidated.append(self.__background.get_rect())

        # Redraw the dynamics
        invalidated.extend(self.dynamics.draw(surface))

        # Redraw the UI on top of everything
        # No need to clear it since its not supposed to move in any way
        # self.ui.clear(surface, self.__background)
        invalidated.extend(self.ui.draw(surface))

        return invalidated

    def draw_statics(self, surface: Surface):
        dynamics_state: Rect = self.dynamics.state
        # self.statics.clear(surface, self.__background)
        surface.blit(self.__background, (-dynamics_state.left, -dynamics_state.top))
        # self.statics.draw(surface)

    def draw_dynamics(self, surface: Surface) -> List[Rect]:
        self.dynamics.clear(surface, self.background)
        return self.dynamics.draw(surface)

    def start(self):
        for go in self.statics.sprites():
            go.start(self)

        for go in self.dynamics.sprites():
            go.start(self)

        for go in self.ui.sprites():
            go.start(self)

    def update(self, delta_time: float):
        # Dispatch updates to every game object
        self.statics.update(delta_time)
        self.dynamics.update(delta_time)
        self.ui.update(delta_time)

        # Center the camera around the player
        # but only if the player has moved enough
        if len(self.player) > 0:
            if self.dynamics.center(self.player.sprite.transform):
                self.__state_dirty = True
