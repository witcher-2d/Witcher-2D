from enum import Enum
from .core.vector2 import Vector2

screen_size = width, height = 640, 480
map_size = Vector2(x=2000, y=1000)
gravity = 0.0005


class Colors(Enum):
    black = (0, 0, 0)
    white = (255, 255, 255)
