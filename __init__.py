import bpy
from . import shp

properties = [
    shp.property.SHP_PG_MaterialItem,
    shp.property.SHP_PG_Action,
    shp.property.SHP_PG_Object,
    shp.property.SHP_PG_Scene,
]

classes = [
    shp.ui.SHP_UL_material_list,
    shp.ui.SHP_UL_action_list,
    shp.panel.SHP_PL_Scene,
    shp.panel.SHP_PL_Material,
    shp.panel.SHP_PL_Object,
    shp.operator.SHP_OT_HouseMaterial_Add,
    shp.operator.SHP_OT_HouseMaterial_Remove,
    shp.operator.SHP_OT_HouseMaterial_NodeGroup_Apply,
    shp.operator.SHP_OT_Renderer_All,
    shp.operator.SHP_OT_Renderer_One,
    shp.operator.SHP_OT_Keyframes_Apply,
]

def register():
    for cls in properties:
        bpy.utils.register_class(cls)

    bpy.types.Scene.shp = bpy.props.PointerProperty(type=shp.property.SHP_PG_Scene)
    bpy.types.Object.shp = bpy.props.PointerProperty(type=shp.property.SHP_PG_Object)
    bpy.types.Action.shp = bpy.props.PointerProperty(type=shp.property.SHP_PG_Action)

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Action.shp
    del bpy.types.Object.shp
    del bpy.types.Scene.shp

    for cls in properties:
        bpy.utils.unregister_class(cls)