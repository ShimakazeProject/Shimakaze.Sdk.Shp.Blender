import bpy

from .settings import SHP_PG_HouseMaterialSettings, SHP_PG_ObjectSettings


class SHP_OT_HouseMaterial_Init(bpy.types.Operator):
    bl_idname = 'shp.house_material_init'
    bl_label = '创建所属色节点组'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        house_material_settings = SHP_PG_HouseMaterialSettings.get_instance()
        if not house_material_settings:
            return {'CANCELLED'}

        house_material_settings.init_materials(context)
        return {'FINISHED'}


class SHP_OT_HouseMaterial_Add(bpy.types.Operator):
    bl_idname = 'shp.house_material_add'
    bl_label = '添加所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        house_material_settings = SHP_PG_HouseMaterialSettings.get_instance()
        if not house_material_settings or not house_material_settings.add_material(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_HouseMaterial_Remove(bpy.types.Operator):
    bl_idname = 'shp.house_material_remove'
    bl_label = '移除所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        house_material_settings = SHP_PG_HouseMaterialSettings.get_instance()
        if not house_material_settings or not house_material_settings.remote_material(context):
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_HouseMaterial_Set_1(bpy.types.Operator):
    bl_idname = 'shp.house_material_set_1'
    bl_label = '阻隔所选对象'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = SHP_PG_HouseMaterialSettings.get_house_materials_from_objects(
            context.selected_objects)
        SHP_PG_HouseMaterialSettings.apply_house_materials(materials, 1)
        return {'FINISHED'}


class SHP_OT_HouseMaterial_Set_0(bpy.types.Operator):
    bl_idname = 'shp.house_material_set_0'
    bl_label = '恢复所选对象'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = SHP_PG_HouseMaterialSettings.get_house_materials_from_objects(
            context.selected_objects)
        SHP_PG_HouseMaterialSettings.apply_house_materials(materials, 0)
        return {'FINISHED'}
