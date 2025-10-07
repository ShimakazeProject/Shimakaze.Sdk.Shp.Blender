import bpy
from .operator import SHP_OT_Object_Add
from .operator import SHP_OT_Object_Remove
from .operator import SHP_OT_HouseMaterial_Add
from .operator import SHP_OT_HouseMaterial_Remove
from .operator import SHP_OT_HouseMaterial_NodeGroup_Apply
from .operator import SHP_OT_Marker_Init
from .operator import SHP_OT_Marker_Add
from .operator import SHP_OT_Marker_Remove
from .props import SHP_PG_MaterialItem
from .props import SHP_PG_ObjectItem
from .props import SHP_PG_MarkerItem
from .props import SHP_PG_RenderSettings
from .panel import SHP_PL_GlobalSettings
from .panel import SHP_PL_Object
from .panel import SHP_PL_Action
from .panel import SHP_PL_Material
from .ui import SHP_UL_material_list
from .ui import SHP_UL_object_list
from .ui import SHP_UL_marker_list

properties = [
    SHP_PG_MaterialItem,
    SHP_PG_ObjectItem,
    SHP_PG_MarkerItem,
    SHP_PG_RenderSettings,
]

classes = [
    SHP_UL_material_list,
    SHP_UL_object_list,
    SHP_UL_marker_list,
    SHP_OT_Object_Add,
    SHP_OT_Object_Remove,
    SHP_OT_HouseMaterial_Add,
    SHP_OT_HouseMaterial_Remove,
    SHP_OT_HouseMaterial_NodeGroup_Apply,
    SHP_OT_Marker_Init,
    SHP_OT_Marker_Add,
    SHP_OT_Marker_Remove,
    SHP_PL_GlobalSettings,
    SHP_PL_Object,
    SHP_PL_Action,
    SHP_PL_Material,
]


def register():
    for cls in properties:
        bpy.utils.register_class(cls)

    bpy.types.Text.shp = bpy.props.PointerProperty(
        type=SHP_PG_RenderSettings)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Text.shp

    for cls in properties:
        bpy.utils.unregister_class(cls)
