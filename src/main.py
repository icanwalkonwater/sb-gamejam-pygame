import time

import pygame
from pygame import Surface, Vector2

from game_object import GameObject
from keyboard_input import InputController
from player import Player
from scene import Scene

FPS_LIMIT = 60
frames = 0


def create_test_scene(screen) -> Scene:
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

    green_box_s = Surface((50, 50))
    green_box_s.fill((0, 255, 0))

    player = Player(green_box_s, .5)
    player.move(Vector2(100, 200))
    player.apply_force(Vector2(500, -1400))

    player.add_to_collision_mask(red_box, orange_box)

    return Scene(background, [red_box, orange_box], [player])


def main():
    pygame.init()

    # Setup screen
    screen: pygame.Surface = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Hey")
    pygame.mouse.set_visible(True)

    # Setup input controller
    input_controller: InputController = InputController(vertical=(pygame.K_SPACE, -1))
    input_controller.acceleration = Vector2(3, 10)

    # Setup scene
    scene = create_test_scene(screen)
    scene.draw_init(screen)  # Initial draw (background)
    scene.dynamics.sprites()[0]._input_controller = input_controller  # Setup player

    # Setup clock
    clock: pygame.time.Clock = pygame.time.Clock()
    clock.tick()

    # Used to
    last_fps_update = time.time()

    # Game loop
    while True:
        delta_time = clock.get_time()

        # Dispatch update through every game objects of the scene
        scene.update(delta_time)

        # Draw pass
        for invalidated in scene.draw_auto(screen):
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
