from pygame import Rect as pyRect
import pygame
from .. import screen_size, gravity
from .base import BaseGameObject
from .position import Position
from ..animation.animator import Animator
from ..animation.frames import FrameRow, Frame
from ..core.rect import Rect

class NPC(BaseGameObject):
    hp = 300
    image_path = 'game/res/Kajdush.png'
    frames = {
        'stay': 1
    }
    animation_speed = 1.0
    speedx = 0
    speedy = 0
    on_gorund = False
    flipx = False
    on_walk = False
    anim_jump = False

    def __init__(self, start_pos=Position(x=200, y=200)):
        super().__init__()
        self.size.x = 64
        self.size.y = 64
        self.pos = start_pos
        self.rect = pyRect(
            self.pos.x, self.pos.y,
            self.size.x, self.size.y
            )
        self.animator = Animator(self.image_path, size=self.size)
        frames_row_stay = FrameRow()
        frames_row_stay.speed = 1.0/7.5

        frames_row_stay.add(Frame(Rect(x=0, y=0, w=64, h=64)))
        self.animator.add_frames_row('stay', frames_row_stay)
        self.animator.set_row('stay')

    def update_anim(self, time):
        self.animator.update_frame(time)
        self.animator.draw()
        print(self.hp)

    @property
    def view_point(self):
        forward = 100
        if self.animator.flipx:
            forward *= -1

        return Position(
            x=self.pos.x + forward,
            y=self.pos.y - 50
        )

    def take_damage(self, damage, td, direction):
        self.hp -= damage
        if direction == 0:
            self.speedx = -200 
        else:
            self.speedx = 200 
        self.speedy -= 40
        self.pos.y += self.speedy * td * 10
        if self.hp <= 0:
            self.destroy()


    def update_pos(self, keys, platforms, td):
        self.on_walk = False
        self.speedy += gravity
        self.pos.y += self.speedy * td

        self.pos.x += self.speedx * td
        if(self.speedx != 0 and self.speedx > 0):
            self.speedx -= 10
        elif(self.speedx != 0 and self.speedx < 0):
            self.speedx += 10
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
            if self.animator.current_frame_name != "stay":
                self.animator.set_row('stay')
            self.on_gorund = True
            self.anim_jump = False

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

        self.rect.x = self.pos.x


