class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def mult_on_scalar(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def quad_mult(self, scalar, param):
        if self.x == 0 or self.y == 0:
            return
        self.x = self.x * (scalar / max(param/self.x, 1))
        self.y = self.y * (scalar / max(param/self.y, 1))

    def normalize(self):
        pass

    @property
    def get_t(self):
        return (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return self.__class__(x=x, y=y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return self.__class__(x=x, y=y)

    def __str__(self):
        return 'x={} y={}'.format(self.x, self.y)
