from .objects.position import Position
from .core.vector2 import Vector2

from . import map_size, screen_size


class Camera(object):

    def __init__(self, screen, center_obj=None):
        self.pos = Position()
        self.screen = screen
        self.screen_size = Vector2(screen_size[0], screen_size[1])
        self.map_maxs = map_size
        self.center_obj = center_obj

    def set_center_obj(self, obj):
        self.center_obj = obj

    def update_pos(self, center_on_hero=True):

        if not self.center_obj or not center_on_hero:
            return
        prev_pos = self.pos
        dest_pos = self.center_obj.view_point
        dest_pos.x =\
            dest_pos.x\
            + int(self.center_obj.size.x/2)\
            - float(self.screen_size.x)/2
        dest_pos.y =\
            dest_pos.y\
            + int(self.center_obj.size.y/2)\
            - float(self.screen_size.y)/2

        dest_pos = Position.smooth_move(prev_pos, dest_pos)
        dest_pos.put_in_rect(
            0,
            0,
            self.map_maxs.x - self.screen_size.x,
            self.map_maxs.y - self.screen_size.y,
        )
        self.pos = dest_pos

    def draw(self, to_draw):
        for o in to_draw:
            self.screen.blit(
                o.animator.surface,
                (
                    o.rect.x - self.pos.x,
                    o.rect.y - self.pos.y,
                )
            )
