from pygame import Surface, SRCALPHA
from pygame.image import load as load_img
from pygame.transform import flip
import pygame
from ..core.vector2 import Vector2
from .frames import FrameRow


class Animator(object):

    def __init__(
            self,
            file_path,
            size=Vector2()):
        self.size = size
        self.file_path = file_path
        self.surface = Surface(self.size.get_t, SRCALPHA)

        self.spritesheet = load_img(file_path)
        self.surface.fill((0, 0, 0, 0))
        self.flipx = False
        self.frames_rows = {}
        self.current_frames_row = None
        self.current_frame_name = None

    def add_frames_row(self, name, frames_row):
        if isinstance(frames_row, FrameRow):
            self.frames_rows[name] = frames_row
        else:
            raise TypeError('Must be FrameRow type')

    def set_row(self, row):
        if row in self.frames_rows:
            self.current_frame_name = row
            self.current_frames_row = self.frames_rows[row]
            self.current_frames_row.current_frame = 0
            self.current_frames_row.last_frame_time = 0
        else:
            raise TypeError('Must be FrameRow type')

    def draw(self):
        self.surface.fill((0, 0, 0, 0))

        self.surface.blit(
            self.spritesheet,
            (0, 0),
            self.current_frames_row.frame
        )
        self.surface = flip(self.surface, self.flipx, False)


    def update_frame(self, time):
        self.current_frames_row.calculate_frame(time)
