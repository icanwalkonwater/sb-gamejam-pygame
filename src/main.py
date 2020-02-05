import time

import pygame
from pygame import Surface, Vector2

from constants import RESOLUTION
from game_object import GameObject
from hostiles.hth_enemy import HthEnemy
from keyboard_input import InputController
from player import Player
from scene import Scene
from scene_management import SceneManagement
from ui.player_bar import UIHealthBar, UIManaBar

FPS_LIMIT = 60

frames = 0


def get_ui(player: Player) -> [GameObject]:
    health_bar = UIHealthBar(player)
    mana_bar = UIManaBar(player)

    return [health_bar, mana_bar]


def create_test_scene(screen: Surface) -> Scene:
    background: Surface = Surface(screen.get_size())
    background.fill((250, 250, 250))

    red_box_s: Surface = Surface((300, 50))
    red_box_s.fill((255, 0, 0))

    red_box: GameObject = GameObject(red_box_s)
    red_box.move(Vector2(50, 250))

    orange_box_s: Surface = Surface((300, 50))
    orange_box_s.fill((255, 100, 0))

    orange_box: GameObject = GameObject(orange_box_s)
    orange_box.move(Vector2(400, 350))

    green_box_s = Surface((30, 50))
    green_box_s.fill((0, 255, 0))

    floor_s: Surface = Surface((1080, 50))
    floor_s.fill((0, 0, 0))
    floor: GameObject = GameObject(floor_s)
    floor.move(Vector2(0, 600))

    wall_left_s: Surface = Surface((50, 100))
    wall_left_s.fill((0, 0, 0))
    wall_left: GameObject = GameObject(wall_left_s)
    wall_left.move(Vector2(0, 500))

    wall_right_s: Surface = Surface((50, 100))
    wall_right_s.fill((0, 0, 0))
    wall_right: GameObject = GameObject(wall_left_s)
    wall_right.move(Vector2(1000, 500))

    player = Player(green_box_s, .5)
    player.move(Vector2(100, 200))

    enemy = HthEnemy(player)
    enemy.move(Vector2(900, 500))

    ui_comps = get_ui(player)

    scene: Scene = Scene(background, [red_box, orange_box, floor, wall_left, wall_right], [player, enemy, *ui_comps])

    scene.environment.add(red_box, orange_box, floor, wall_left, wall_right)
    scene.player.add(player)
    scene.enemies.add(enemy)
    scene.ui.add(*ui_comps)

    player.add_to_collision_mask(scene.environment, scene.enemies)
    enemy.add_to_collision_mask(scene.environment)

    return scene


def main():
    pygame.init()

    # Setup screen
    screen: pygame.Surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Hey")
    pygame.mouse.set_visible(True)

    # Setup input controller
    InputController.init(vertical=(pygame.K_SPACE, -1), acceleration=Vector2(5, 1))

    # Setup scene management
    SceneManagement.init({
        'main': create_test_scene(screen)
    })
    SceneManagement.load_scene('main', screen)

    # Setup clock
    clock: pygame.time.Clock = pygame.time.Clock()
    clock.tick()

    # Used to
    last_fps_update = time.time()

    # Game loop
    while True:
        delta_time = clock.get_time()

        # Update inputs
        InputController.update()
        # Dispatch update through every game objects of the scene
        SceneManagement.active_scene.update(delta_time)

        # Draw pass
        for invalidated in SceneManagement.active_scene.draw_auto(screen):
            pygame.display.update(invalidated)

        # Update the screen
        pygame.display.flip()

        # Reset the clock
        if time.time() - last_fps_update > 1:
            last_fps_update = time.time()
            print(f'\rFPS: {int(clock.get_fps())}    ', end='')
        global frames
        frames += 1
        clock.tick(FPS_LIMIT)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    except KeyboardInterrupt:
        print(f'\nFrames: {frames}, mean FPS: {frames / (time.time() - start_time)}')
