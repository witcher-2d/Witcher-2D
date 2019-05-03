class ObjectList(object):

    def __init__(self):
        self.objects = []

    def add_item(self, item):
        self.objects.append(item)

    def add_list_condition(self, items, condition=lambda x: True):
        'condition must be a function wich applys to item'

        self.objects = [*self.objects, *[item for item in items if condition(item)]]   # NOQA

    def remove_item(self, item):
        if item in self.objects:
            self.objects.remove(item)


class ObjectManager(object):

    def __init__(self):
        self.to_draw = ObjectList()
        self.to_update_pos = ObjectList()

    def load_object(self, obj):
        if callable(obj):
            obj = obj()

        # TODO: check if obj is game object and have all base functions
        obj.object_manager = self
        if obj.is_drawable:
            self.to_draw.add_item(obj)
        if obj.is_movable:
            self.to_update_pos.add_item(obj)

    def load_list(self, obj_list, is_drawable=True, is_movable=False):
        for obj in obj_list:
            obj.object_manager = self
            if obj.is_drawable:
                self.to_draw.add_item(obj)
            if obj.is_movable:
                self.to_update_pos.add_item(obj)

    def destroy_object(self, obj):
        self.to_draw.remove_item(obj)
        self.to_update_pos.remove_item(obj)
