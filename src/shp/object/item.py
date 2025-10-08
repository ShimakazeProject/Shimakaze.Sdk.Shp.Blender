from __future__ import annotations
import bpy

class SHP_PG_Object(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(
        name='Object', type=bpy.types.Object)