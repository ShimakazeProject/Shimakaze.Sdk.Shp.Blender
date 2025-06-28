import bpy

from ... import property

class SHP_OT_HouseMaterial_Add(bpy.types.Operator):
    bl_idname = 'shp.house_material_add'
    bl_label = '添加所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene: property.SHP_PG_Scene = context.scene.shp
        if not scene.target:
            return {'CANCELLED'}
        
        object: property.SHP_PG_Object = scene.target.shp

        mat = context.active_object.active_material
        if not mat:
            return {'CANCELLED'}
        
        # TODO: 优化逻辑
        for item in object.house_materials:
            if item.material == mat:
                return {'CANCELLED'}

        slot = object.house_materials.add()
        slot.material = mat
        object.active_house_material_index += 1
        
        return {'FINISHED'}