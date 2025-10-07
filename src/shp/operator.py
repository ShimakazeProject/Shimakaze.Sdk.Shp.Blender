import bpy

from .props import SHP_PG_RenderSettings
from .props import SHP_PG_ObjectItem
from .props import SHP_PG_MaterialItem


class SHP_OT_Object_Add(bpy.types.Operator):
    bl_idname = 'shp.object_add'
    bl_label = '添加对象'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
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
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.remote_object(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_HouseMaterial_Add(bpy.types.Operator):
    bl_idname = 'shp.house_material_add'
    bl_label = '添加所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.add_material(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_HouseMaterial_Remove(bpy.types.Operator):
    bl_idname = 'shp.house_material_remove'
    bl_label = '移除所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.remote_material(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_HouseMaterial_NodeGroup_Apply(bpy.types.Operator):
    bl_idname = 'shp.house_material_node_group_apply'
    bl_label = '创建所属色节点组'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()

        if not settings:
            return {'CANCELLED'}

        settings.init_materials(context)
        return {'FINISHED'}

class SHP_OT_Marker_Init(bpy.types.Operator):
    bl_idname = 'shp.marker_init'
    bl_label = '刷新时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.init_markers(context):
            return {'CANCELLED'}

        return {'FINISHED'}

class SHP_OT_Marker_Add(bpy.types.Operator):
    bl_idname = 'shp.marker_add'
    bl_label = '创建时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.add_marker(context):
            return {'CANCELLED'}

        return {'FINISHED'}

class SHP_OT_Marker_Remove(bpy.types.Operator):
    bl_idname = 'shp.marker_remove'
    bl_label = '删除时间标记'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = SHP_PG_RenderSettings.get_instance()
        if not settings:
            return {'CANCELLED'}
        if not settings.remove_marker(context):
            return {'CANCELLED'}

        return {'FINISHED'}