from __future__ import annotations
import bpy

class SHP_PG_HouseMaterial(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(
        name='Material', type=bpy.types.Material)