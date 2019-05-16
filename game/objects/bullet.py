from pygame import Rect as pyRect
from .position import Position
from .base import BaseGameObject
from .. import screen_size
from ..animation.animator import Animator
from ..animation.frames import Frame, FrameRow
from ..core.rect import Rect


class Bullet(BaseGameObject):
    image_path = 'game/res/bullet.png'
    speed = 700

    def __init__(self, hero):
        super().__init__()
        self.size.x = 10
        self.size.y = 10
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
        frames_row.add(Frame(Rect(x=0, y=0, w=10, h=10)))
        self.animator.add_frames_row('stay', frames_row)
        self.animator.set_row('stay')
        self.animator.draw()

    def update_pos(self, time):
        if self.direction:
            self.pos.x += self.speed * time
        else:
            self.pos.x -= self.speed * time
        self.rect.x = self.pos.x

        if self.pos.x < 0 or self.pos.y < 0 or\
                self.pos.x > screen_size[0] - self.rect.w or \
                self.pos.y > screen_size[1] - self.rect.h:
            self.destroy()
