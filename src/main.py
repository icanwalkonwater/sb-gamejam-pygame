import time

import pygame
from pygame import Surface, Vector2

from constants import GlobalSettings
from game_objects.entities.hostiles.hth_enemy import HthEnemy
from game_objects.entities.hostiles.ranged_enemy import RangedEnemy
from game_objects.entities.player import Player
from game_objects.entities.player_management import PlayerManagement
from game_objects.environement_props import ButtonGameObject, WindGameObject
from game_objects.game_object import GameObject
from keyboard_input import InputController
from music_manager import MusicManager
from scene import Scene
from scene_loader import SceneLoader
from scene_management import SceneManagement
from ui.player_bar import UIHealthBar, UIManaBar

FPS_LIMIT = 60
frames = 0


def get_ui(player: Player) -> [GameObject]:
    health_bar = UIHealthBar()
    mana_bar = UIManaBar()

    return [health_bar, mana_bar]


def create_test_scene(screen: Surface) -> Scene:
    background: Surface = Surface((3000, 3000))
    background.fill((250, 250, 250))

    red_box_s: Surface = Surface((300, 50))
    red_box_s.fill((255, 0, 0))

    red_box: GameObject = GameObject(red_box_s)
    red_box.move(Vector2(50, 250))

    orange_box_s: Surface = Surface((300, 50))
    orange_box_s.fill((255, 100, 0))

    orange_box: GameObject = GameObject(orange_box_s)
    orange_box.move(Vector2(400, 350))

    floor_s: Surface = Surface((1080, 50))
    floor_s.fill((0, 0, 0))
    floor: GameObject = GameObject(floor_s)
    floor.move(Vector2(0, 600))

    button: ButtonGameObject = ButtonGameObject()
    button.move(Vector2(500, 580))

    wall_left_s: Surface = Surface((50, 100))
    wall_left_s.fill((0, 0, 0))
    wall_left: GameObject = GameObject(wall_left_s)
    wall_left.move(Vector2(0, 500))

    wall_right_s: Surface = Surface((50, 100))
    wall_right_s.fill((0, 0, 0))
    wall_right: GameObject = GameObject(wall_left_s)
    wall_right.move(Vector2(1000, 500))

    wind_stream: WindGameObject = WindGameObject((200, 200), Vector2(1, 0), 20)
    wind_stream.move(Vector2(950, 200))

    player = Player()
    player.move(Vector2(100, 200))

    enemy = HthEnemy()
    enemy.move(Vector2(900, 500))

    enemy2 = RangedEnemy()
    enemy2.move(Vector2(600, 500))

    ui_comps = get_ui(player)

    scene: Scene = Scene(background, [red_box, orange_box, floor, wall_left, wall_right],
                         [player, enemy, enemy2, button, wind_stream], ui_comps)

    scene.environment.add(red_box, orange_box, floor, wall_left, wall_right)

    return scene


def main():
    pygame.init()

    # Setup screen
    screen: pygame.Surface = pygame.display.set_mode(GlobalSettings.RESOLUTION)
    pygame.display.set_caption('Les Aventures de Voronof')
    pygame.mouse.set_visible(True)

    # Setup input controller
    InputController.init(vertical=(pygame.K_SPACE, -1), acceleration=Vector2(5, 1))

    PlayerManagement.init(Player())

    # Setup scene management
    SceneManagement.init({
        'main': create_test_scene(screen),
        'main_menu': SceneLoader('levels/main_menu.xml', {
            'start': lambda btn: btn.on_enter.append(lambda: SceneManagement.load_scene('level_1'))
        }).parse_all(),
        'level_test': SceneLoader('levels/level_test.xml').parse_all(),
        'vision_test': SceneLoader('levels/vision_test.xml').parse_all(),
        'level_1': SceneLoader('levels/level_1_tutorial.xml').parse_all(),
        'level_2': SceneLoader('levels/level_2_tutorial.xml').parse_all()
    })
    SceneManagement.load_scene('main_menu')

    # Setup clock
    clock: pygame.time.Clock = pygame.time.Clock()
    clock.tick()

    # Used to
    last_fps_update = time.time()

    # start the music
    MusicManager.init()

    # Game loop
    while True:
        delta_time = clock.get_time()

        # Update inputs
        InputController.update()
        # Dispatch update through every game objects of the scene
        SceneManagement.active_scene.update(delta_time)

        # Draw pass
        draw_pass()
        # cProfile.run('draw_pass()')

        # Reset the clock
        if time.time() - last_fps_update > 1:
            last_fps_update = time.time()
            print(f'\rFPS: {int(clock.get_fps())}    ', end='')
        global frames
        frames += 1
        clock.tick(FPS_LIMIT)


# Draw pass
def draw_pass():
    for invalidated in SceneManagement.active_scene.draw_auto(pygame.display.get_surface()):
        pygame.display.update(invalidated)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    except KeyboardInterrupt:
        print(f'\nFrames: {frames}, mean FPS: {frames / (time.time() - start_time)}')
