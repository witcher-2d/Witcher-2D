from pygame import Rect as pyRect
from .position import Position
from .base import BaseGameObject
from .. import screen_size
from ..animation.animator import Animator
from ..animation.frames import Frame, FrameRow
from ..core.rect import Rect
from ..core.vector2 import Vector2
from .hero import Hero
from .NPC import NPC

class Bomb(BaseGameObject):
    image_path = 'game/res/bomb.png'

    def __init__(self, hero):
        super().__init__()
        self.speed = Vector2(x=300, y=-250)
        self.size.x = 32
        self.size.y = 32
        self.is_movable = True
        self.pos = Position()
        self.pos.x = hero.pos.x
        self.pos.y = hero.pos.y + 20
        self.rect = pyRect(
            self.pos.x, self.pos.y,
            self.size.x, self.size.y
            )
        self.direction = not hero.animator.flipx
        if self.direction:
            self.pos.x += hero.size.x

        self.animator = Animator(self.image_path, size=self.size)
        frames_row = FrameRow()
        frames_row.add(Frame(Rect(x=0, y=0, w=32, h=32)))
        self.animator.add_frames_row('stay', frames_row)
        self.animator.set_row('stay')
        self.animator.draw()

    def update_pos(self, time, to_destroy):
        if self.direction:
            self.pos.x += self.speed.x * time
        else:
            self.pos.x -= self.speed.x * time
        self.speed.y += 10
        self.pos.y += self.speed.y * time
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.pos.x < 0 or self.pos.y < 0 or\
                self.pos.x > screen_size[0] - self.rect.w or \
                self.pos.y > screen_size[1] - self.rect.h:
            self.destroy()
        for item in to_destroy:
            if self.rect.colliderect(item.rect) and isinstance(item, NPC):
                    item.take_damage(20, time, self.direction)
            if self.rect.colliderect(item.rect) and not isinstance(item, Hero) and not isinstance(item, Bomb):
                self.destroy()
