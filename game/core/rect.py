from pygame.rect import Rect as pyRect


class Rect(object):

    def __init__(self, x=0, y=0, w=10, h=10, pos=None, size=None, rect=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if pos:
            self.x = pos.x
            self.y = pos.y

        if size:
            self.w = size.x
            self.h = size.y

        if rect:
            self.x = rect.x
            self.y = rect.y
            self.w = rect.w
            self.h = rect.h

    @property
    def pyrect(self):
        rect = pyRect()
        rect.x = self.x
        rect.y = self.y
        rect.w = self.w
        rect.h = self.h
        return rect

    @property
    def get_t(self):
        return (self.x, self.y, self.w, self.h)
