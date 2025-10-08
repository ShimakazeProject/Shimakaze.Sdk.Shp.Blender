import bpy

from .settings import SHP_PG_ActionSettings


class SHP_OT_Action_Init(bpy.types.Operator):
    bl_idname = 'shp.action_init'
    bl_label = '刷新时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_ActionSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.init_actions(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_Action_Add(bpy.types.Operator):
    bl_idname = 'shp.action_add'
    bl_label = '创建时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_ActionSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.add_action(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_Action_Remove(bpy.types.Operator):
    bl_idname = 'shp.action_remove'
    bl_label = '删除时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_ActionSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.remove_action(context):
            return {'CANCELLED'}

        return {'FINISHED'}
