from .position import Position
from ..core.vector2 import Vector2


class BaseGameObject(object):

    def __init__(self):
        self.is_drawable = True
        self.is_movable = False
        self.object_manager = None
        self.pos = Position()
        self.size = Vector2()

    def get_center(self):
        return self.pos

    def destroy(self):
        if not self.object_manager:
            raise IndexError('No object to destroy')
        self.object_manager.destroy_object(self)
