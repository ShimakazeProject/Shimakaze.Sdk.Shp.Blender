import bpy

from .action import *
from .object import *
from .house_material import *
from .render_task import *
from .settings import *
from .ui import *

classes = [
    SHP_PG_Action,
    SHP_PG_ActionSettings,
    SHP_UL_action_list,
    SHP_PT_Action,
    SHP_OT_Action_Add,
    SHP_OT_Action_Init,
    SHP_OT_Action_Remove,
    SHP_PG_Object,
    SHP_PG_ObjectSettings,
    SHP_UL_object_list,
    SHP_PT_Object,
    SHP_OT_Object_Add,
    SHP_OT_Object_Remove,
    SHP_PG_HouseMaterial,
    SHP_PG_HouseMaterialSettings,
    SHP_UL_house_material_list,
    SHP_PT_HouseMaterial,
    SHP_OT_HouseMaterial_Init,
    SHP_OT_HouseMaterial_Add,
    SHP_OT_HouseMaterial_Remove,
    SHP_OT_HouseMaterial_Set_0,
    SHP_OT_HouseMaterial_Set_1,
    SHP_PG_RenderTask,
    SHP_PG_RenderQueue,
    SHP_UL_render_list,
    SHP_PT_RenderQueue,
    SHP_OT_RenderQueue_Add,
    SHP_OT_RenderQueue_Remove,
    SHP_OT_RenderQueue_Render,
    SHP_PG_GlobalSettings,
    SHP_PT_GlobalSettings,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Text.shp = bpy.props.PointerProperty(
        type=SHP_PG_GlobalSettings)


def unregister():
    del bpy.types.Text.shp

    for cls in classes:
        bpy.utils.unregister_class(cls)
