from .position import Position
from pygame import Rect as pyRect
from .base import BaseGameObject
from ..animation.animator import Animator
from ..animation.frames import FrameRow, Frame
from ..core.rect import Rect


class Image(BaseGameObject):
    image_path = 'game/res/Sky.png'
    pos = Position()

    def __init__(self, start_pos, image_path):
        super().__init__()
        self.size.x = 1000
        self.size.y = 1000
        self.pos = start_pos
        self.rect = pyRect(
            self.pos.x, self.pos.y,
            self.size.x, self.size.y
            )
        self.animator = Animator(self.image_path, size=self.size)
        frames_row = FrameRow()
        frames_row.add(Frame(Rect(x=0, y=0, w=1000, h=1000)))
        self.animator.add_frames_row('stay', frames_row)
        self.animator.set_row('stay')
        self.animator.draw()