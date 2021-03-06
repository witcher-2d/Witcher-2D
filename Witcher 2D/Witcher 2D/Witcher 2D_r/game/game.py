import sys
import pygame
import time
from . import Colors, screen_size, map_size
from .objects.hero import Hero
from .objects.bullet import Bullet
from .objects.platform import Platform
from .objects.position import Position
from .camera import Camera
from .object_manager import ObjectManager
from pygame import key


def start():
    pygame.init()
    obj_manager = ObjectManager()

    screen = pygame.display.set_mode(screen_size)
    hero = Hero()
    camera = Camera(screen, center_obj=hero)
    obj_manager.load_objcet(hero)
    platforms = []
    for i in range(10):
        platforms.append(Platform(Position(x=0+i*50, y=300)))
    obj_manager.load_list(platforms)

    cur_time = time.time()
    time_delta = 0
    last_frame_time = 0
    to_shoot = True
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = key.get_pressed()
        last_frame_time += time_delta
#        while last_frame_time > 1:
#            to_shoot = True
#            last_frame_time = 0
#        if keys[pygame.K_a] and to_shoot:
#            to_shoot = False
#            bullet = Bullet(hero)
#            obj_manager.load_objcet(bullet)

        time_delta = time.time()-cur_time
        cur_time = time.time()
        for item in obj_manager.to_update_pos.objects:
            item.update_pos(time_delta)
        hero.update_pos(keys, platforms, time_delta)
        hero.update_anim(time_delta)
        camera.update_pos()

        screen.fill(Colors.black.value)
        camera.draw(obj_manager.to_draw.objects)
        pygame.display.flip()
