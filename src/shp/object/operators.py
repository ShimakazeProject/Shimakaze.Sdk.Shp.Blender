import bpy

from .settings import SHP_PG_ObjectSettings

class SHP_OT_Object_Add(bpy.types.Operator):
    bl_idname = 'shp.object_add'
    bl_label = '添加对象'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_ObjectSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.add_objects(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_Object_Remove(bpy.types.Operator):
    bl_idname = 'shp.object_remove'
    bl_label = '移除对象'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_ObjectSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.remote_object(context):
            return {'CANCELLED'}

        return {'FINISHED'}