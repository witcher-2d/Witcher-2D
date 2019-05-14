from enum import Enum
from .core.vector2 import Vector2

screen_size = width, height = 1080, 720
map_size = Vector2(x=10000, y=1000)
gravity = 10


class Colors(Enum):
    black = (0, 0, 0)
    white = (255, 255, 255)
