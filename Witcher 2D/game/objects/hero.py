from pygame import Rect as pyRect
import pygame
from .. import screen_size, gravity
from .base import BaseGameObject
from .position import Position
from ..animation.animator import Animator
from ..animation.frames import FrameRow, Frame
from ..core.rect import Rect
from .dialog import showDialog
from ..pygame_functions import *
import random


class Hero(BaseGameObject):
    image_path = 'game/res/hero_spritesheet.png'
    frames = {
        'stay': 4,
        'walk': 4,
        'jump': 4,
        'jump_wsword': 4,
        'stay_wsword': 4,
        'walk_wsword': 4,
        'draw_the_sword': 4,
        'attack_wsword': 2,
        'hide_the_sword': 4,
        'attack': 3,

    }
    animation_speed = 1.0
    speedx = 100
    speedy = 0
    on_gorund = False
    flipx = False
    on_walk = False
    anim_jump = False
    sword = False
    sword_time = 0

    def __init__(self, start_pos=Position(x=100, y=100)):
        super().__init__()
        self.size.x = 43
        self.size.y = 64
        self.pos = start_pos
        self.rect = pyRect(
            self.pos.x, self.pos.y,
            self.size.x, self.size.y
            )
        self.animator = Animator(self.image_path, size=self.size)
        frames_row_stay = FrameRow()
        frames_row_stay.speed = 1.0/7.5
        for i in range(4):
            frames_row_stay.add(Frame(Rect(x=0 + 42*i, y=0, w=42 + 42*i, h=62)))
        self.animator.add_frames_row('stay', frames_row_stay)
        self.animator.set_row('stay')
        frames_row_jump = FrameRow()
        frames_row_jump.speed = 1.0/5
        for i in range(4):
            frames_row_jump.add(Frame(Rect(x=0 + 42*i, y=64, w=42 + 42*i, h=64)))
        self.animator.add_frames_row('jump', frames_row_jump)
        frames_row_walk = FrameRow()
        frames_row_walk.speed = 1.0/7.5
        for i in range(4):
            frames_row_walk.add(Frame(Rect(x=0 + 42*i, y=128, w=42 + 42*i, h=128)))
        self.animator.add_frames_row('walk', frames_row_walk)
        frames_row_stay_wsword = FrameRow()
        frames_row_stay_wsword.speed = 1.0 / 7.5
        for i in range(4):
            frames_row_stay_wsword.add(Frame(Rect(x=0 + 42 * i, y=261, w=42 + 42 * i, h=64)))
        self.animator.add_frames_row('stay_wsword', frames_row_stay_wsword)
        frames_row_jump_wsword = FrameRow()
        frames_row_jump_wsword.speed = 1.0 / 5
        for i in range(4):
            frames_row_jump_wsword.add(Frame(Rect(x=0 + 48 * i, y=326, w=46 + 48 * i, h=64)))
        self.animator.add_frames_row('jump_wsword', frames_row_jump_wsword)
        frames_row_walk_wsword = FrameRow()
        frames_row_walk_wsword.speed = 1.0 / 7.5
        for i in range(4):
            frames_row_walk_wsword.add(Frame(Rect(x=0 + 42 * i, y=390, w=42 + 42 * i, h=128)))
        self.animator.add_frames_row('walk_wsword', frames_row_walk_wsword)
        frames_row_draw_the_sword = FrameRow()
        frames_row_draw_the_sword.speed = 1.0 / 7.5
        for i in range(4):
            frames_row_draw_the_sword.add(Frame(Rect(x=0 + 42 * i, y=390, w=42 + 42 * i, h=128)))
        self.animator.add_frames_row('draw_the_sword', frames_row_draw_the_sword)
        frames_row_attack = FrameRow()
        frames_row_attack.speed = 1.0 / 7.5
        for i in range(3):
            frames_row_attack.add(Frame(Rect(x=0 + 42 * i, y=454, w=42 + 42 * i, h=64)))
        self.animator.add_frames_row('attack', frames_row_attack)
    def update_anim(self, time):
        self.animator.update_frame(time)
        self.animator.draw()

    @property
    def view_point(self):
        forward = 100
        if self.animator.flipx:
            forward *= -1

        return Position(
            x=self.pos.x + forward,
            y=self.pos.y - 50
        )

    def update_pos(self, keys, platforms, td):
        self.on_walk = False
        self.speedy += gravity
        if keys[pygame.K_SPACE] and self.on_gorund:
            self.speedy = -250
            self.current_frame = 0
            self.anim_jump = True
            if self.sword == False:
                self.animator.set_row('jump')
            else:
                self.animator.set_row('jump_wsword')
        if keys[pygame.K_a]:
            if self.sword == False:
                if self.animator.current_frame_name != "walk" and self.on_gorund and not self.anim_jump:
                    self.animator.set_row('walk')
            else:
                if self.animator.current_frame_name != "walk_wsword" and self.on_gorund and not self.anim_jump:
                    self.animator.set_row('walk_wsword')
            self.pos.x -= self.speedx * td
            self.animator.flipx = True
            self.on_walk = True
        if keys[pygame.K_d]:
            if self.sword == False:
                if self.animator.current_frame_name != "walk" and self.on_gorund and not self.anim_jump:
                    self.animator.set_row('walk')
            else:
                if self.animator.current_frame_name != "walk_wsword" and self.on_gorund and not self.anim_jump:
                    self.animator.set_row('walk_wsword')
            self.pos.x += self.speedx * td
            self.animator.flipx = False
            self.on_walk = True
        if keys[pygame.K_c]:
            if self.sword_time > 1:
                self.sword_time = 0
                if self.sword == False:
                    self.animator.set_row('draw_the_sword')
                    self.sword = True
                else:
                    self.sword = False
        if keys[pygame.K_g]:
            newL = makeLabel("Hello, i am Reva.",48,50,50,"blue","Agency FB","white")
            showLabel(newL)
        self.pos.y += self.speedy * td
        self.sword_time += td
        self.on_gorund = False
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.x > screen_size[0] - self.rect.w:
            self.pos.x = screen_size[0] - self.rect.w
        if self.pos.y > screen_size[1] - self.rect.h:
            self.pos.y = screen_size[1] - self.rect.h
            self.speedy = 0
            if self.sword == False:
                if self.animator.current_frame_name != "stay":
                    self.animator.set_row('stay')
            else:
                if self.animator.current_frame_name != "stay_wsword":
                    self.animator.set_row('stay_wsword')
            self.on_gorund = True
            self.anim_jump = False

        self.rect.y = self.pos.y
        for item in platforms:
            if self.rect.colliderect(item.rect):
                if (self.speedy > 0):
                    self.rect.y = item.rect.y - self.rect.h
                    self.speedy = 0

                    self.on_gorund = True
                    if self.sword == False:
                        if self.animator.current_frame_name != "stay" and not keys[pygame.K_d] and not keys[pygame.K_a]:
                            self.animator.set_row('stay')
                    else:
                        if self.animator.current_frame_name != "stay_wsword" and not keys[pygame.K_d] and not keys[pygame.K_a]:
                            self.animator.set_row('stay_wsword')
                    self.anim_jump = False
                    self.pos.y = self.rect.y
                if (self.speedy < 0):
                    self.rect.y = item.rect.y + item.rect.h
                    self.speedy = 0
                    self.pos.y = self.rect.y

        self.rect.x = self.pos.x
        for item in platforms:
            if self.rect.colliderect(item.rect):
                if (keys[pygame.K_d]):
                    self.rect.x = item.rect.x - self.rect.w
                    self.pos.x = self.rect.x
                if (keys[pygame.K_a]):
                    self.rect.x = item.rect.x + item.rect.w
                    self.pos.x = self.rect.x
