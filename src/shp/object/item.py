from __future__ import annotations
import typing
import bpy


class SHP_PG_Object(bpy.types.PropertyGroup):
    def update_object(self, context: bpy.types.Context):
        self.name = self.object.name

    object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Object',
        update=update_object,)
