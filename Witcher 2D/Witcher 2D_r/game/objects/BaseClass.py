from pygame import Surface, SRCALPHA
from pygame import Rect
from pygame.image import load as load_img
from pygame.transform import flip
import pygame
from .. import Colors
from .. import screen_size, gravity
from .position import Position
from .. import map_size


class NPC(object):
    size = (50, 63)
    image_path = 'Witcher 2D_r/game/res/Zeppily.jpg'
    frames = {
        'stay': 1,
        'walk': 1,
        'jump': 1
    }
    animation_speed = 0.15
    speedx = 200
    speedy = 0
    on_walk = False
    anim_jump = False
    on_ground = False
    flipx = False
    pos = Position()
    def __init__(self, start_pos=Position(x=0, y=100)):
        self.surface = Surface(self.size, SRCALPHA)
        self.spritesheet = load_img(self.image_path)
        self.surface.fill((0, 0, 0, 0))
        self.pos = start_pos
        self.rect = Rect(
            self.pos.x, self.pos.y,
            self.size[0], self.size[1]
            )
        self.current_frame = 0
        self.last_frame_time = 0
    def update_anim(self, time):
            self.last_frame_time += time
            if self.anim_jump:
                row = 0
                frames = self.frames['jump']
            else:
                if self.on_walk:
                    row = 0
                    frames = self.frames['walk']
                else:
                    row = 0
                    frames = self.frames['stay']

                while self.last_frame_time > self.animation_speed:
                    self.current_frame += 1
                    self.last_frame_time = self.last_frame_time - self.animation_speed
                if not self.anim_jump:
                    self.current_frame = self.current_frame % frames
                else:
                    self.current_frame = min(self.current_frame, frames)
            self.surface.fill((0, 0, 0, 0))
            self.surface.blit(
                self.spritesheet,
                (0, 0),
                (
                    0*self.current_frame,
                    0,
                    0, 0
                )
            )
            self.surface = flip(self.surface, self.flipx, False)
    def update_pos(self, keys, platforms,td):
        self.on_walk = False
        self.speedy += gravity
   
        self.pos.y += self.speedy
        self.on_ground = False

        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.x > map_size.x - self.rect.w:
            self.pos.x = map_size.x - self.rect.w
        if self.pos.y > map_size.y - self.rect.h:
            self.pos.y = map_size.y - self.rect.h
            self.speedy = 0
            self.on_gorund = True
            self.anim_jump = False
        self.on_gorund = False
        self.rect.x = self.pos.x

        self.rect.y = self.pos.y
        for item in platforms:           
            if self.rect.colliderect(item.rect):
                if (self.speedy > 0):
                    self.rect.y = item.rect.y - self.rect.h
                    self.speedy = 0
                    self.on_gorund = True
                    self.anim_jump = False
                    self.pos.y = self.rect.y
                if (self.speedy < 0):
                    self.rect.y = item.rect.y + item.rect.h
                    self.speedy = 0
                    self.pos.y = self.rect.y

    def put_on_screen(self, screen):
        screen.blit(self.surface, self.rect)
