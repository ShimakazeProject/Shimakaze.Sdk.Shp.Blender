from __future__ import annotations
import typing
import bpy

from .item import SHP_PG_Object


class SHP_PG_ObjectSettings(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_ObjectSettings | None:
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings:
            return settings.object

    objects: bpy.props.CollectionProperty(
        name='对象', type=SHP_PG_Object)
    current_object_index: bpy.props.IntProperty(
        name='当前选中的对象')

    def get_objects(self):
        objects: typing.Set[bpy.types.Object] = set()
        for slot in self.objects:
            slot: SHP_PG_Object
            object: bpy.types.Object = slot.object
            objects.add(object)
            for child in object.children_recursive:
                objects.add(child)

        return objects

    def add_objects(self, context: bpy.types.Context):
        objects = filter(lambda object: not self.objects.get(
            object.name), context.selected_objects)

        for object in objects:
            slot: SHP_PG_Object = self.objects.add()
            slot.object = object

        return True

    def remote_object(self, context: bpy.types.Context):
        if self.current_object_index < 0 or self.current_object_index >= len(self.objects):
            return False

        self.objects.remove(self.current_object_index)
        self.current_object_index = max(
            0, self.current_object_index - 1)

        return True
