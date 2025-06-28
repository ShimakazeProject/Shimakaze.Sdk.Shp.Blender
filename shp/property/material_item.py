import bpy

# 中间 PropertyGroup，用于包装对材质的引用
class SHP_PG_MaterialItem(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(name='Material', type=bpy.types.Material)