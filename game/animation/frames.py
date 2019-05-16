from ..core.rect import Rect
from .animation_types import AnimationType


class Frame(object):
    def __init__(self, rect=Rect()):
        self.rect = rect


class FrameRow(object):

    def __init__(self):
        self.frames = []
        self.animation_type = AnimationType.sycled
        self.speed = 1.0/25
        self.last_frame_time = 0
        self.current_frame = 0

    def add(self, frame):
        if isinstance(frame, Frame):
            self.frames.append(frame)
        else:
            raise TypeError('Need Frame type to append')

    def calculate_frame(self, time):
        self.last_frame_time += time
        while self.last_frame_time > self.speed:
            self.current_frame += 1
            self.last_frame_time = self.last_frame_time - self.speed
        if self.animation_type == AnimationType.sycled:
            self.current_frame = self.current_frame % len(self.frames)
        elif self.animation_type == AnimationType.stop:
            self.current_frame = min(self.current_frame, len(self.frames) - 1)

    @property
    def frame(self):
        return self.frames[self.current_frame].rect.get_t
