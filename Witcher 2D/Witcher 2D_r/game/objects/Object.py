from pygame import Surface, SRCALPHA
from pygame import Rect
from pygame.image import load as load_img
from pygame.transform import flip
import pygame
from .. import Colors
from .. import screen_size, gravity
from .position import Position

class NPC(object):
    size = (50, 64)
    frames = {
        'stay': 1
    }
    image_path = "Witcher 2D_r/game/res/Zeppily.jpg"
    animation_speed = 0.25
    speedx = 0
    speedy = 0
    on_ground = False
    flip_x = False
    pos = Position()

    def __init__(self, start_pos):
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

        self.surface.blit(self.spritesheet, (0, 0))

    def update_anim(self, time):
        self.last_frame_time += time
        row = 0
        frames = self.frames['stay']

        while self.last_frame_time > self.animation_speed:
            self.current_frame += 1
            self.last_frame_time = self.last_frame_time - self.animation_speed
        else:
            self.current_frame = min(self.current_frame, frames)
            self.surface.fill((0, 0, 0, 0))
            self.surface.blit(
                self.spritesheet,
                (0, 0),
                (
                    0*self.current_frame,
                    0,
                    43, 64
                )
            )
            self.surface = flip(self.surface, self.flip_x, False)
    def update_pos(self, keys, platforms,td):
        self.on_walk = False
        self.speedy += gravity
        self.pos.y += self.speedy
        self.on_ground = False
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.x > screen_size[0] - self.rect.w:
            self.pos.x = screen_size[0] - self.rect.w
        if self.pos.y > screen_size[1] - self.rect.h:
            self.pos.y = screen_size[1] - self.rect.h
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
                    self.pos.y = self.rect.y
                if (self.speedy < 0):
                    self.rect.y = item.rect.y + item.rect.h
                    self.speedy = 0
                    self.pos.y = self.rect.y

    def put_on_screen(self, screen):
        screen.blit(self.surface, self.rect)
